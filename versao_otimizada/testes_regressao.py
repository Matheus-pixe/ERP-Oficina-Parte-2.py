"""Execute com python testes_regressao.py, na pasta da versão otimizada."""
import io
import unittest
from contextlib import redirect_stdout
from decimal import Decimal
from unittest.mock import patch

import main
import Parte_Rani as clientes
from estruturas.arvore_avl import ArvoreAVL
from estruturas.fila_prioridade import FilaPrioridade
from models.ordem_servico import OrdemServico
from services import ordem_service as os_service


def menu(*linhas):
    saida = io.StringIO()
    with patch("builtins.input", side_effect=linhas), redirect_stdout(saida):
        main.main()
    return saida.getvalue()


class TestesRegressao(unittest.TestCase):
    def setUp(self):
        for modulo, nome, novo in (
            (clientes, "cadastro", []),
            (os_service, "ordens", ArvoreAVL()),
            (os_service, "fila_ordens", FilaPrioridade()),
        ):
            substituicao = patch.object(modulo, nome, novo)
            substituicao.start()
            self.addCleanup(substituicao.stop)

    def test_renomear_preserva_clientes_e_veiculos(self):
        clientes.cadastro.extend([["Ana", [["ABC1234", "Gol"]]], ["Bia", []]])
        menu("1", "1", "4", "Ana", " bIA ", "6", "0", "0")
        self.assertEqual(clientes.cadastro, [["Ana", [["ABC1234", "Gol"]]], ["Bia", []]])
        menu("1", "1", "4", "Ana", "ANA", "6", "0", "0")
        self.assertEqual(clientes.cadastro[0][0], "ANA")

    def test_campos_obrigatorios_da_os(self):
        for indice in range(3):
            with self.subTest(campo=indice):
                dados = ["Ana", "Gol", "Freio"]
                dados[indice] = "   "
                menu("3", "1", "1", *dados, "0", "0")
                self.assertIsNone(os_service.ordens.buscar(1))
                self.assertTrue(os_service.fila_ordens.esta_vazia())

    def test_empate_em_centavos_respeita_ordem_de_cadastro(self):
        saida = menu("3", "1", "20", "Ana", "Gol", "Freio", "2",
                     "1", "10", "Bia", "Uno", "Óleo", "2",
                     "6", "20", "A", "0,10", "6", "20", "B", "0,20",
                     "6", "10", "C", "0,30", "10", "0", "0")
        relatorio = saida.split("--- RELATÓRIO POR VALOR ---")[1]
        self.assertLess(relatorio.index("OS 20 |"), relatorio.index("OS 10 |"))
        self.assertEqual(os_service.ordens.buscar(20).valor_total, Decimal("0.30"))

    def test_valor_invalido_preserva_servicos_e_total(self):
        menu("3", "1", "20", "Ana", "Gol", "Freio", "2",
             "6", "20", "A", "12,34", "6", "20", "B", "NaN",
             "6", "20", "C", "1e999999999", "6", "20", "D", "-0,01",
             "6", "20", "E", "0,001", "0", "0")
        ordem = os_service.ordens.buscar(20)
        self.assertEqual(ordem.valor_total, Decimal("12.34"))
        self.assertEqual(len(ordem.servicos), 1)

    def test_total_fora_da_precisao_preserva_ordem(self):
        ordem = OrdemServico(1, "A", "B", "C", 2)
        limite = Decimal("9" * 26 + ".99")
        ordem.adicionar_servico("Primeiro serviço", limite)
        with self.assertRaises(ValueError):
            ordem.adicionar_servico("Outro serviço", "0.01")
        ordem.calcular_valor()
        self.assertEqual(ordem.valor_total, limite)
        self.assertEqual(len(ordem.servicos), 1)

    def test_duplicata_na_fila(self):
        fila = FilaPrioridade()
        ordem = OrdemServico(1, "A", "B", "C", 2)
        fila.inserir(ordem)
        fila.inserir(ordem)
        self.assertIs(fila.remover_maior_prioridade(), ordem)
        self.assertTrue(fila.esta_vazia())

    def test_posicao_em_outra_fila(self):
        a, b = FilaPrioridade(), FilaPrioridade()
        primeira = OrdemServico(1, "A", "B", "C", 2)
        segunda = OrdemServico(2, "D", "E", "F", 3)
        a.inserir(primeira)
        b.inserir(segunda)
        with self.assertRaises(ValueError):
            b.inserir(primeira)
        self.assertFalse(b.remover(primeira))
        b.atualizar_prioridade(primeira)
        self.assertIs(b.remover_maior_prioridade(), segunda)
        self.assertIs(a.remover_maior_prioridade(), primeira)


if __name__ == "__main__":
    unittest.main(verbosity=2)

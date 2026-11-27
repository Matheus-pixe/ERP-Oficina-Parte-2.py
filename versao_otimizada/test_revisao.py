import contextlib
import io
import unittest
from unittest.mock import patch
from math import isfinite
import pecas
import Parte_Rani
from services import ordem_service as service
from models.ordem_servico import OrdemServico
from estruturas.fila_prioridade import FilaPrioridade
from estruturas.arvore_avl import ArvoreAVL


def executar(funcao, entradas=()):
    with patch('builtins.input', side_effect=entradas), contextlib.redirect_stdout(io.StringIO()) as saida:
        funcao()
    return saida.getvalue()


class Revisao(unittest.TestCase):
    def setUp(self):
        pecas.pecas.clear()
        pecas.historico_movimentacoes.clear()
        Parte_Rani.cadastro.clear()
        service.ordens = ArvoreAVL()
        service.fila_ordens = FilaPrioridade()

    def ordem(self, codigo=1):
        ordem = OrdemServico(codigo, 'Ana', 'Carro', 'Revisao', 3)
        service.ordens.inserir(codigo, ordem)
        service.fila_ordens.inserir(ordem)
        return ordem

    def test_fila_insercao_repetida(self):
        ordem = self.ordem()
        service.fila_ordens.inserir(ordem)
        self.assertEqual(service.fila_ordens.tamanho(), 1)
        self.assertIs(service.fila_ordens.remover_maior_prioridade(), ordem)
        self.assertTrue(service.fila_ordens.esta_vazia())
        self.assertEqual(ordem.pos_fila, -1)

    def test_remocao_em_outra_fila(self):
        ordem = self.ordem()
        outra = FilaPrioridade()
        self.assertFalse(outra.remover(ordem))
        outra.atualizar_prioridade(ordem)
        self.assertEqual(service.fila_ordens.tamanho(), 1)

    def test_soma_nao_pode_virar_infinito(self):
        ordem = self.ordem()
        executar(service.registrar_servico, ['1', 'Primeiro', '1e308'])
        executar(service.registrar_servico, ['1', 'Segundo', '1e308'])
        self.assertTrue(isfinite(ordem.valor_total))
        self.assertEqual(len(ordem.servicos), 1)

    def test_ajuste_manual_nao_desfaz_movimento_antigo(self):
        executar(pecas.cadastro_pecas, ['Pneu', '10', '20'])
        executar(pecas.saida_estoque, ['Pneu', '3'])
        executar(pecas.alteracao_pecas, ['Pneu', '100', ''])
        executar(pecas.desfazer_ultima_movimentacao)
        self.assertEqual(pecas.pecas[0]['Quantidade: '], 100)

    def test_alterar_preco_preserva_desfazer(self):
        executar(pecas.cadastro_pecas, ['Pneu', '10', '20'])
        executar(pecas.saida_estoque, ['Pneu', '3'])
        executar(pecas.alteracao_pecas, ['Pneu', '', '30'])
        executar(pecas.desfazer_ultima_movimentacao)
        self.assertEqual(pecas.pecas[0]['Quantidade: '], 10)

    def test_movimento_novo_apos_ajuste(self):
        executar(pecas.cadastro_pecas, ['Pneu', '10', '20'])
        executar(pecas.saida_estoque, ['Pneu', '3'])
        executar(pecas.alteracao_pecas, ['Pneu', '100', ''])
        executar(pecas.entrada_estoque, ['Pneu', '5'])
        executar(pecas.desfazer_ultima_movimentacao)
        self.assertEqual(pecas.pecas[0]['Quantidade: '], 100)

    def test_status_e_fila(self):
        ordem = self.ordem()
        for status in ('2', '3', '1', '1'):
            executar(service.alterar_status, ['1', status])
            self.assertEqual(service.fila_ordens.tamanho(), int(status == '1'))
        executar(service.processar_proxima_ordem)
        self.assertEqual(ordem.status, 'Em manutenção')
        self.assertEqual(ordem.pos_fila, -1)

    def test_renomear_cliente_duplicado(self):
        Parte_Rani.cadastro.extend([['Ana', []], ['Bia', []]])
        executar(Parte_Rani.menu_clientes, ['4', 'Ana', 'bia', '6'])
        self.assertEqual([x[0] for x in Parte_Rani.cadastro], ['Ana', 'Bia'])

    def test_campos_vazios_os(self):
        for campo in range(3):
            valores = ['Ana', 'Carro', 'Revisao']
            valores[campo] = '  '
            executar(service.cadastrar_ordem, ['1'] + valores)
            self.assertEqual(len(service.ordens), 0)

    def test_valores_invalidos_sem_mutacao(self):
        ordem = self.ordem()
        for valor in ('nan', 'inf', '-1', 'abc'):
            executar(service.registrar_servico, ['1', 'Servico', valor])
        self.assertEqual(ordem.servicos, [])
        self.assertEqual(ordem.valor_total, 0)

    def test_peca_recadastrada_nao_recebe_desfazer_antigo(self):
        executar(pecas.cadastro_pecas, ['Pneu', '10', '20'])
        executar(pecas.saida_estoque, ['Pneu', '3'])
        executar(pecas.remocao_pecas, ['Pneu', 's'])
        executar(pecas.cadastro_pecas, ['Pneu', '50', '20'])
        executar(pecas.desfazer_ultima_movimentacao)
        self.assertEqual(pecas.pecas[0]['Quantidade: '], 50)

if __name__ == '__main__':
    unittest.main(verbosity=2)

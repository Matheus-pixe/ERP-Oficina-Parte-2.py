"""Testes da versao otimizada e da equivalencia com a versao base.

Rodar a partir da raiz do repositorio:
    python testes/testes_otimizacoes.py

Os testes usam apenas a biblioteca padrao (unittest). Nenhum codigo do sistema
depende deste arquivo: ele so confere se as estruturas novas estao corretas e
se as duas versoes produzem os mesmos resultados.
"""
import importlib.util
import math
import os
import random
import subprocess
import sys
import unittest

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
BASE = os.path.join(RAIZ, "versao_base")
OTIM = os.path.join(RAIZ, "versao_otimizada")

sys.path.insert(0, AQUI)
import roteiros


def carregar(nome, pasta, *caminho):
    """Carrega um unico .py por caminho, sem misturar os pacotes das duas versoes."""
    arquivo = os.path.join(pasta, *caminho)
    spec = importlib.util.spec_from_file_location(nome, arquivo)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


avl = carregar("otim_avl", OTIM, "estruturas", "arvore_avl.py")
fila_otim = carregar("otim_fila", OTIM, "estruturas", "fila_prioridade.py")
fila_base = carregar("base_fila", BASE, "estruturas", "fila_prioridade.py")
ord_otim = carregar("otim_ord", OTIM, "algoritmos", "ordenacao.py")
ord_base = carregar("base_ord", BASE, "algoritmos", "ordenacao.py")
modelo = carregar("otim_modelo", OTIM, "models", "ordem_servico.py")


# ---------------------------------------------------------------- AVL

def verificar_avl(no, minimo=None, maximo=None):
    """Confere ordem de busca, altura guardada e fator de balanceamento. Devolve a altura."""
    if no is None:
        return 0

    assert minimo is None or no.chave > minimo, "viola a ordem de busca"
    assert maximo is None or no.chave < maximo, "viola a ordem de busca"

    altura_esq = verificar_avl(no.esquerda, minimo, no.chave)
    altura_dir = verificar_avl(no.direita, no.chave, maximo)

    assert abs(altura_esq - altura_dir) <= 1, "arvore desbalanceada"

    altura = 1 + (altura_esq if altura_esq > altura_dir else altura_dir)
    assert no.altura == altura, "altura guardada errada"

    return altura


def chaves(lista_de_ordens):
    return [o.codigo for o in lista_de_ordens]


def nova_ordem(codigo, prioridade=3, valor=0):
    o = modelo.OrdemServico(codigo, f"cli{codigo}", "v", "p", prioridade)
    o.valor_total = valor
    return o


def arvore_com(*codigos):
    arvore = avl.ArvoreAVL()
    for c in codigos:
        arvore.inserir(c, nova_ordem(c))
    return arvore


class TestesAVL(unittest.TestCase):

    def test_rotacoes_simples_e_duplas(self):
        # cada sequencia obriga um tipo de rotacao e a raiz final tem que ser 20
        casos = {
            "direita-direita (rotacao esquerda)": (10, 20, 30),
            "esquerda-esquerda (rotacao direita)": (30, 20, 10),
            "esquerda-direita (rotacao dupla)": (30, 10, 20),
            "direita-esquerda (rotacao dupla)": (10, 30, 20),
        }
        for nome, sequencia in casos.items():
            with self.subTest(nome):
                arvore = arvore_com(*sequencia)
                self.assertEqual(arvore.raiz.chave, 20)
                self.assertEqual(arvore.altura(), 2)
                verificar_avl(arvore.raiz)

    def test_travessias_arvore_conhecida(self):
        arvore = arvore_com(30, 20, 40, 10, 25, 35, 50)
        self.assertEqual(chaves(arvore.em_ordem()), [10, 20, 25, 30, 35, 40, 50])
        self.assertEqual(chaves(arvore.pre_ordem()), [30, 20, 10, 25, 40, 35, 50])
        self.assertEqual(chaves(arvore.pos_ordem()), [10, 25, 20, 35, 50, 40, 30])

    def test_travessias_com_nivel(self):
        arvore = arvore_com(30, 20, 40, 10)
        niveis = [(n, o.codigo) for n, o in arvore.pre_ordem(com_nivel=True)]
        self.assertEqual(niveis, [(0, 30), (1, 20), (2, 10), (1, 40)])

    def test_arvore_vazia(self):
        arvore = avl.ArvoreAVL()
        self.assertEqual(len(arvore), 0)
        self.assertTrue(arvore.esta_vazia())
        self.assertIsNone(arvore.buscar(1))
        self.assertIsNone(arvore.remover(1))
        self.assertEqual(arvore.em_ordem(), [])
        self.assertEqual(arvore.pre_ordem(), [])
        self.assertEqual(arvore.pos_ordem(), [])
        self.assertEqual(arvore.altura(), 0)

    def test_chave_duplicada_nao_sobrescreve(self):
        arvore = avl.ArvoreAVL()
        primeira = nova_ordem(5)
        self.assertTrue(arvore.inserir(5, primeira))
        self.assertFalse(arvore.inserir(5, nova_ordem(5)))
        self.assertEqual(len(arvore), 1)
        self.assertIs(arvore.buscar(5), primeira)

    def test_busca_existente_e_inexistente(self):
        arvore = arvore_com(8, 3, 10, 1, 6)
        self.assertEqual(arvore.buscar(6).codigo, 6)
        self.assertIsNone(arvore.buscar(7))
        self.assertIsNone(arvore.buscar(-1))

    def test_remocao_folha_um_filho_dois_filhos_e_raiz(self):
        arvore = arvore_com(50, 30, 70, 20, 40, 60, 80, 10)
        for chave in (10, 20, 30, 50, 80):  # folha, um filho, dois filhos, raiz...
            removida = arvore.remover(chave)
            self.assertEqual(removida.codigo, chave)
            self.assertIsNone(arvore.buscar(chave))
            verificar_avl(arvore.raiz)
        self.assertEqual(chaves(arvore.em_ordem()), [40, 60, 70])
        self.assertEqual(len(arvore), 3)

    def test_remover_inexistente(self):
        arvore = arvore_com(1, 2, 3)
        self.assertIsNone(arvore.remover(99))
        self.assertEqual(len(arvore), 3)

    def test_fuzz_contra_lista_de_referencia(self):
        rng = random.Random(2024)
        arvore = avl.ArvoreAVL()
        referencia = []  # lista simples com busca linear

        for passo in range(4000):
            chave = rng.randint(0, 250)
            operacao = rng.randint(1, 3)

            if operacao == 1:
                existia = chave in referencia
                self.assertEqual(arvore.inserir(chave, nova_ordem(chave)), not existia)
                if not existia:
                    referencia.append(chave)

            elif operacao == 2:
                removida = arvore.remover(chave)
                if chave in referencia:
                    self.assertEqual(removida.codigo, chave)
                    referencia.remove(chave)
                else:
                    self.assertIsNone(removida)

            else:
                achou = arvore.buscar(chave)
                self.assertEqual(achou is not None, chave in referencia)

            self.assertEqual(len(arvore), len(referencia))

            if passo % 50 == 0:
                verificar_avl(arvore.raiz)
                em_ordem = chaves(arvore.em_ordem())
                for i in range(1, len(em_ordem)):
                    self.assertLess(em_ordem[i - 1], em_ordem[i])
                self.assertEqual(len(em_ordem), len(referencia))

        verificar_avl(arvore.raiz)

    def test_altura_logaritmica_em_pior_caso_para_arvore_comum(self):
        n = 10000
        limite = 1.4405 * math.log2(n + 2) - 0.3277  # altura maxima teorica de uma AVL
        for nome, sequencia in (("crescente", range(1, n + 1)),
                                ("decrescente", range(n, 0, -1))):
            with self.subTest(nome):
                arvore = avl.ArvoreAVL()
                for c in sequencia:
                    arvore.inserir(c, nova_ordem(c))
                self.assertLessEqual(arvore.altura(), limite)
                self.assertEqual(len(arvore), n)
                verificar_avl(arvore.raiz)


# ---------------------------------------------------------------- Merge Sort

def lote_com_empates(n, semente):
    """Ordens na 'ordem de chegada', com muitas prioridades e valores repetidos."""
    rng = random.Random(semente)
    codigos = list(range(1, n + 1))
    rng.shuffle(codigos)
    return [nova_ordem(c, rng.randint(1, 5), rng.randint(0, 6) * 50.0) for c in codigos]


class TestesMergeSort(unittest.TestCase):

    def test_mesmo_resultado_do_bubble_sort_da_base(self):
        casos = (("prioridade", "ordenar_por_prioridade"),
                 ("valor", "ordenar_por_valor"),
                 ("codigo", "ordenar_por_codigo"))

        for n in (0, 1, 2, 3, 10, 57, 300):
            lista = lote_com_empates(n, semente=n)  # ordem de chegada
            # a otimizada recebe as ordens em qualquer ordem (como vem da arvore)
            embaralhada = lista.copy()
            random.Random(n + 1).shuffle(embaralhada)

            for nome, funcao in casos:
                with self.subTest(criterio=nome, n=n):
                    esperado = getattr(ord_base, funcao)(lista)
                    obtido = getattr(ord_otim, funcao)(embaralhada)
                    self.assertEqual([id(o) for o in obtido], [id(o) for o in esperado])

    def test_ordenar_por_chegada(self):
        lista = lote_com_empates(100, semente=5)
        embaralhada = lista.copy()
        random.Random(6).shuffle(embaralhada)
        obtido = ord_otim.ordenar_por_chegada(embaralhada)
        self.assertEqual([id(o) for o in obtido], [id(o) for o in lista])

    def test_nao_altera_a_lista_original(self):
        lista = lote_com_empates(50, semente=9)
        antes = [id(o) for o in lista]
        ord_otim.ordenar_por_valor(lista)
        ord_otim.ordenar_por_prioridade(lista)
        self.assertEqual([id(o) for o in lista], antes)

    def test_merge_sort_generico(self):
        rng = random.Random(3)
        numeros = [rng.randint(0, 100) for _ in range(500)]
        resultado = ord_otim.merge_sort(numeros, lambda esq, dir: esq > dir)
        for i in range(1, len(resultado)):
            self.assertLessEqual(resultado[i - 1], resultado[i])
        self.assertEqual(len(resultado), len(numeros))


# ---------------------------------------------------------------- Heap

def verificar_heap(fila):
    for i, ordem in enumerate(fila.fila):
        assert ordem.pos_fila == i, "pos_fila desatualizada"
        if i > 0:
            pai = fila.fila[(i - 1) // 2]
            assert not fila._tem_precedencia(ordem, pai), "propriedade do heap violada"


class TestesHeap(unittest.TestCase):

    def test_empate_sai_por_ordem_de_chegada(self):
        fila = fila_otim.FilaPrioridade()
        ordens = [nova_ordem(c, 4) for c in (7, 3, 9, 1)]
        for o in ordens:
            fila.inserir(o)
        saida = [fila.remover_maior_prioridade().codigo for _ in range(4)]
        self.assertEqual(saida, [7, 3, 9, 1])
        self.assertIsNone(fila.remover_maior_prioridade())
        self.assertTrue(fila.esta_vazia())

    def test_fuzz_contra_fila_da_base(self):
        rng = random.Random(77)
        base = fila_base.FilaPrioridade()
        otim = fila_otim.FilaPrioridade()
        # dois conjuntos independentes de objetos com os mesmos dados
        na_fila_base = []
        na_fila_otim = []
        proximo = 1

        for _ in range(6000):
            op = rng.randint(1, 10)

            if op <= 4:  # inserir
                prioridade = rng.randint(1, 5)
                ob = nova_ordem(proximo, prioridade)
                oo = nova_ordem(proximo, prioridade)
                base.inserir(ob)
                otim.inserir(oo)
                na_fila_base.append(ob)
                na_fila_otim.append(oo)
                proximo += 1

            elif op <= 6:  # processar a proxima
                eb = base.remover_maior_prioridade()
                eo = otim.remover_maior_prioridade()
                if eb is None:
                    self.assertIsNone(eo)
                else:
                    self.assertEqual(eb.codigo, eo.codigo)
                    na_fila_base = [o for o in na_fila_base if o is not eb]
                    na_fila_otim = [o for o in na_fila_otim if o is not eo]

            elif op <= 8 and na_fila_base:  # mudar a prioridade de uma ordem que esta na fila
                i = rng.randint(0, len(na_fila_base) - 1)
                nova = rng.randint(1, 5)
                na_fila_base[i].alterar_prioridade(nova)       # a base nao faz mais nada
                na_fila_otim[i].alterar_prioridade(nova)
                otim.atualizar_prioridade(na_fila_otim[i])     # a otimizada reordena o heap

            elif na_fila_base:  # remover uma ordem especifica da fila
                i = rng.randint(0, len(na_fila_base) - 1)
                codigo = na_fila_base[i].codigo
                self.assertTrue(base.remover_por_codigo(codigo))
                if rng.randint(0, 1):
                    self.assertTrue(otim.remover(na_fila_otim[i]))
                else:
                    self.assertTrue(otim.remover_por_codigo(codigo))
                na_fila_base.pop(i)
                na_fila_otim.pop(i)

            self.assertEqual(base.tamanho(), otim.tamanho())
            verificar_heap(otim)

        # esvazia as duas filas: tem que sair exatamente na mesma ordem
        while not base.esta_vazia():
            self.assertEqual(base.remover_maior_prioridade().codigo,
                             otim.remover_maior_prioridade().codigo)
        self.assertTrue(otim.esta_vazia())

    def test_remover_ordem_que_nao_esta_na_fila(self):
        fila = fila_otim.FilaPrioridade()
        o = nova_ordem(1)
        self.assertFalse(fila.remover(o))
        fila.inserir(o)
        fila.remover_maior_prioridade()
        self.assertEqual(o.pos_fila, -1)
        self.assertFalse(fila.remover(o))
        fila.atualizar_prioridade(o)  # nao deve quebrar
        self.assertFalse(fila.remover_por_codigo(1))


# ---------------------------------------------------------------- ponta a ponta

def rodar(pasta, linhas, script=None):
    """Roda o programa de uma versao com o roteiro e devolve a saida (texto)."""
    arquivo = os.path.join(AQUI, "_roteiro_tmp.txt")
    with open(arquivo, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas))

    try:
        if script is None:
            comando = [sys.executable, "-I", os.path.join(AQUI, "executar_roteiro.py"), pasta, arquivo]
        else:
            codigo = ("import runpy, sys; sys.path.insert(0, sys.argv[1]);"
                      "runpy.run_path(sys.argv[1] + '/' + sys.argv[2], run_name='__main__')")
            comando = [sys.executable, "-I", "-c", codigo, pasta, script]

        resultado = subprocess.run(comando, capture_output=True, text=True, encoding="utf-8")
    finally:
        os.remove(arquivo)

    assert resultado.returncode == 0, resultado.stdout[-800:] + resultado.stderr[-2000:]
    return resultado.stdout


def sem_menu_novo(saida):
    return "\n".join(l for l in saida.split("\n")
                     if not l.startswith(("11 - Exibir", "12 - Exibir", "13 - Exibir")))


class TestesPontaAPonta(unittest.TestCase):

    def test_sessao_completa_gera_a_mesma_saida(self):
        # cadastros, empates, mudanca de prioridade, remocoes, relatorios, clientes, pecas e historico
        linhas = roteiros.completo()
        saida_base = rodar(BASE, linhas)
        saida_otim = rodar(OTIM, linhas)
        self.assertGreater(len(saida_base.split("\n")), 500)
        self.assertEqual(sem_menu_novo(saida_otim), saida_base)

    def test_script_teste_py_da_parte_1_continua_funcionando(self):
        self.assertEqual(rodar(OTIM, [], script="teste.py"), rodar(BASE, [], script="teste.py"))

    def test_opcoes_novas_de_travessia(self):
        saida = rodar(OTIM, roteiros.ordens(travessias=True) + ["0"])
        # as tres travessias aparecem depois da ultima listagem; separa pelos titulos
        em_ordem = saida.split("TRAVESSIA EM ORDEM")[1].split("---")[1]
        pre_ordem = saida.split("TRAVESSIA PRÉ-ORDEM")[1].split("---")[1]
        pos_ordem = saida.split("TRAVESSIA PÓS-ORDEM")[1].split("---")[1]

        def codigos(trecho):
            return [int(l.split("OS")[1].split("|")[0]) for l in trecho.split("\n") if "OS " in l]

        c_em, c_pre, c_pos = codigos(em_ordem), codigos(pre_ordem), codigos(pos_ordem)

        self.assertEqual(len(c_em), len(c_pre))
        self.assertEqual(len(c_em), len(c_pos))
        for i in range(1, len(c_em)):
            self.assertLess(c_em[i - 1], c_em[i])                # em ordem: crescente
        self.assertEqual(c_pre[0], c_pos[-1])                    # raiz: primeira na pre, ultima na pos
        self.assertEqual(sorted_manual(c_pre), c_em)             # mesmos registros
        self.assertEqual(sorted_manual(c_pos), c_em)


def sorted_manual(lista):
    """Ordena por insercao so para o teste conferir conjuntos (sem usar sort/sorted)."""
    resultado = []
    for x in lista:
        i = len(resultado)
        while i > 0 and resultado[i - 1] > x:
            i -= 1
        resultado.insert(i, x)
    return resultado


if __name__ == "__main__":
    unittest.main(verbosity=2)

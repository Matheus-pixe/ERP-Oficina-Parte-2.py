"""Mede o desempenho de UMA versao do sistema (base ou otimizada).

Normalmente nao e chamado direto: use benchmark/comparar.py, que mede as duas.

uso: python -I benchmark/medir.py --versao base|otimizada --saida arquivo.json
         [--tamanhos 100 1000 5000 10000] [--repeticoes 5] [--semente 42] [--sem-contagem]

Como a medicao e feita
  * as operacoes sao as mesmas que o services/ordem_service.py executa (cadastro com
    checagem de codigo repetido, consulta, remocao, relatorios, processar proxima OS),
    chamadas direto nas estruturas, sem input() e print() no meio do tempo medido;
  * tempo: time.perf_counter, coletor de lixo desligado durante a medicao, 1 repeticao de
    aquecimento descartada e N repeticoes registradas (media e desvio padrao amostral);
  * comparacoes: contadas em UMA execucao a parte, com tipos int/float que contam cada
    comparacao de chave (==, !=, <, <=, >, >=). O codigo das versoes NAO e alterado;
  * digest: resumo (hash) dos resultados de cada operacao, para o comparar.py provar que as
    duas versoes devolveram exatamente os mesmos resultados.
"""
import argparse
import gc
import hashlib
import json
import math
import os
import platform
import subprocess
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)

import gerar_dados

OPERACOES = (
    "inserir",
    "busca_existente",
    "busca_inexistente",
    "relatorio_prioridade",
    "relatorio_valor",
    "listagem_por_codigo",
    "listagem_cadastro",
    "remocao",
    "processar_fila",
)


# ---------------------------------------------------------------- contagem de comparacoes

class Contador:
    n = 0


def _contar(metodo):
    def comparar(self, outro):
        Contador.n += 1
        return metodo(self, outro)
    return comparar


class IntC(int):
    __slots__ = ()
    __eq__ = _contar(int.__eq__)
    __ne__ = _contar(int.__ne__)
    __lt__ = _contar(int.__lt__)
    __le__ = _contar(int.__le__)
    __gt__ = _contar(int.__gt__)
    __ge__ = _contar(int.__ge__)
    __hash__ = int.__hash__


class FloatC(float):
    __slots__ = ()
    __eq__ = _contar(float.__eq__)
    __ne__ = _contar(float.__ne__)
    __lt__ = _contar(float.__lt__)
    __le__ = _contar(float.__le__)
    __gt__ = _contar(float.__gt__)
    __ge__ = _contar(float.__ge__)
    __hash__ = float.__hash__


# ---------------------------------------------------------------- adaptadores das versoes

class M:
    """Espaco de nomes preenchido por carregar_versao()."""


class RegistroBase:
    """Faz o mesmo que ordem_service.py da versao base: lista + busca linear + fila por varredura."""

    def __init__(self):
        self.ordens = []
        self.fila = M.FilaPrioridade()

    def inserir(self, ordem):
        if M.buscar_indice(self.ordens, ordem.codigo) != -1:
            return False
        self.ordens.append(ordem)
        self.fila.inserir(ordem)
        return True

    def buscar(self, codigo):
        indice = M.buscar_indice(self.ordens, codigo)
        if indice == -1:
            return None
        return self.ordens[indice]

    def remover(self, codigo):
        indice = M.buscar_indice(self.ordens, codigo)
        if indice == -1:
            return False
        self.ordens.pop(indice)
        self.fila.remover_por_codigo(codigo)
        return True

    def relatorio_prioridade(self):
        return M.ordenar_por_prioridade(self.ordens)

    def relatorio_valor(self):
        return M.ordenar_por_valor(self.ordens)

    def listagem_por_codigo(self):
        return M.ordenar_por_codigo(self.ordens)

    def listagem_cadastro(self):
        return list(self.ordens)


class RegistroOtimizado:
    """Faz o mesmo que ordem_service.py da versao otimizada: AVL + Merge Sort + heap."""

    def __init__(self):
        self.ordens = M.ArvoreAVL()
        self.fila = M.FilaPrioridade()

    def inserir(self, ordem):
        if self.ordens.buscar(ordem.codigo) is not None:
            return False
        self.ordens.inserir(ordem.codigo, ordem)
        self.fila.inserir(ordem)
        return True

    def buscar(self, codigo):
        return self.ordens.buscar(codigo)

    def remover(self, codigo):
        ordem = self.ordens.buscar(codigo)
        if ordem is None:
            return False
        self.ordens.remover(codigo)
        self.fila.remover(ordem)
        return True

    def relatorio_prioridade(self):
        return M.ordenar_por_prioridade(self.ordens.em_ordem())

    def relatorio_valor(self):
        return M.ordenar_por_valor(self.ordens.em_ordem())

    def listagem_por_codigo(self):
        return self.ordens.em_ordem()

    def listagem_cadastro(self):
        return M.ordenar_por_chegada(self.ordens.em_ordem())


def carregar_versao(versao):
    pasta = os.path.join(RAIZ, "versao_base" if versao == "base" else "versao_otimizada")
    sys.path.insert(0, pasta)

    from models.ordem_servico import OrdemServico
    from algoritmos.ordenacao import (ordenar_por_prioridade, ordenar_por_valor,
                                      ordenar_por_codigo)
    from estruturas.fila_prioridade import FilaPrioridade

    M.OrdemServico = OrdemServico
    M.ordenar_por_prioridade = ordenar_por_prioridade
    M.ordenar_por_valor = ordenar_por_valor
    M.ordenar_por_codigo = ordenar_por_codigo
    M.FilaPrioridade = FilaPrioridade

    if versao == "base":
        from algoritmos.busca import buscar_ordem_por_codigo
        M.buscar_indice = buscar_ordem_por_codigo
        M.Registro = RegistroBase
    else:
        from algoritmos.ordenacao import ordenar_por_chegada
        from estruturas.arvore_avl import ArvoreAVL
        M.ordenar_por_chegada = ordenar_por_chegada
        M.ArvoreAVL = ArvoreAVL
        M.Registro = RegistroOtimizado


# ---------------------------------------------------------------- medicao

def criar_ordens(massa, contar):
    ordens = []
    for codigo, cliente, veiculo, problema, prioridade, valor in massa:
        if contar:
            codigo = IntC(codigo)
            prioridade = IntC(prioridade)
        ordem = M.OrdemServico(codigo, cliente, veiculo, problema, prioridade)
        ordem.valor_total = FloatC(valor) if contar else valor
        if contar and hasattr(ordem, "chegada"):
            ordem.chegada = IntC(ordem.chegada)
        ordens.append(ordem)
    return ordens


def digest(valores):
    texto = ",".join(str(int(v)) for v in valores)
    return hashlib.sha256(texto.encode()).hexdigest()[:16]


def cronometrar(funcao):
    gc.collect()
    gc.disable()
    inicio = time.perf_counter()
    resultado = funcao()
    fim = time.perf_counter()
    gc.enable()
    return fim - inicio, resultado


def rodar_uma(massa, existentes, inexistentes, a_remover, contar, com_digest):
    """Executa cada operacao uma vez e devolve {operacao: {tempo, n_ops, comparacoes, digest}}."""
    saida = {}
    ordens = criar_ordens(massa, contar)
    registro = M.Registro()

    def chaves(lista):
        return [IntC(c) for c in lista] if contar else lista

    def anotar(operacao, funcao, n_ops, resumo):
        if contar:
            Contador.n = 0
        segundos, resultado = cronometrar(funcao)
        comparacoes = Contador.n if contar else None
        saida[operacao] = {
            "tempo": segundos,
            "n_ops": n_ops,
            "comparacoes": comparacoes,
            "digest": digest(resumo(resultado)) if com_digest else None,
        }

    def inserir():
        inseridas = 0
        for ordem in ordens:
            if registro.inserir(ordem):
                inseridas += 1
        return inseridas

    anotar("inserir", inserir, len(ordens), lambda r: [r])

    chaves_existentes = chaves(existentes)

    def busca_existente():
        achadas = 0
        for codigo in chaves_existentes:
            if registro.buscar(codigo) is not None:
                achadas += 1
        return achadas

    anotar("busca_existente", busca_existente, len(chaves_existentes), lambda r: [r])

    chaves_inexistentes = chaves(inexistentes)

    def busca_inexistente():
        achadas = 0
        for codigo in chaves_inexistentes:
            if registro.buscar(codigo) is not None:
                achadas += 1
        return achadas

    anotar("busca_inexistente", busca_inexistente, len(chaves_inexistentes), lambda r: [r])

    codigos_da_lista = lambda lista: [o.codigo for o in lista]

    anotar("relatorio_prioridade", registro.relatorio_prioridade, 1, codigos_da_lista)
    anotar("relatorio_valor", registro.relatorio_valor, 1, codigos_da_lista)
    anotar("listagem_por_codigo", registro.listagem_por_codigo, 1, codigos_da_lista)
    anotar("listagem_cadastro", registro.listagem_cadastro, 1, codigos_da_lista)

    chaves_remocao = chaves(a_remover)

    def remocao():
        removidas = 0
        for codigo in chaves_remocao:
            if registro.remover(codigo):
                removidas += 1
        return removidas

    anotar("remocao", remocao, len(chaves_remocao), lambda r: [r])

    if com_digest:
        # fora do cronometro: confere o que sobrou na fila depois das remocoes
        restantes = [saida["remocao"]["digest"]]
        while True:
            ordem = registro.fila.remover_maior_prioridade()
            if ordem is None:
                break
            restantes.append(int(ordem.codigo))
        saida["remocao"]["digest"] = digest(restantes[1:]) + ":" + restantes[0]

    # processar a fila inteira usa uma fila nova, cheia (a montagem nao entra no tempo)
    outras = criar_ordens(massa, contar)
    fila = M.FilaPrioridade()
    for ordem in outras:
        fila.inserir(ordem)

    def processar_fila():
        processadas = []
        while True:
            ordem = fila.remover_maior_prioridade()
            if ordem is None:
                break
            processadas.append(ordem.codigo)
        return processadas

    anotar("processar_fila", processar_fila, len(outras), lambda r: r)

    return saida


def media(valores):
    return sum(valores) / len(valores)


def desvio_padrao(valores):
    if len(valores) < 2:
        return 0.0
    m = media(valores)
    return math.sqrt(sum((v - m) ** 2 for v in valores) / (len(valores) - 1))


def medir_versao(versao, tamanhos, repeticoes, semente, contar):
    carregar_versao(versao)
    resultados = {}

    for n in tamanhos:
        resultados[str(n)] = {}
        existentes = gerar_dados.codigos_existentes(n, semente)
        inexistentes = gerar_dados.codigos_inexistentes(n, semente)
        a_remover = gerar_dados.codigos_para_remover(n, semente)

        for cenario in gerar_dados.CENARIOS:
            massa = gerar_dados.gerar_massa(n, cenario, semente)
            print(f"[{versao}] n={n} cenario={cenario}: aquecimento", flush=True)
            rodar_uma(massa, existentes, inexistentes, a_remover, False, False)

            tempos = {op: [] for op in OPERACOES}
            digests = {}
            n_ops = {}

            for r in range(repeticoes):
                print(f"[{versao}] n={n} cenario={cenario}: repeticao {r + 1}/{repeticoes}",
                      flush=True)
                saida = rodar_uma(massa, existentes, inexistentes, a_remover, False, r == 0)
                for op in OPERACOES:
                    tempos[op].append(saida[op]["tempo"])
                    n_ops[op] = saida[op]["n_ops"]
                    if r == 0:
                        digests[op] = saida[op]["digest"]

            comparacoes = {}
            if contar:
                print(f"[{versao}] n={n} cenario={cenario}: contagem de comparacoes", flush=True)
                saida = rodar_uma(massa, existentes, inexistentes, a_remover, True, False)
                comparacoes = {op: saida[op]["comparacoes"] for op in OPERACOES}

            resultados[str(n)][cenario] = {}
            for op in OPERACOES:
                resultados[str(n)][cenario][op] = {
                    "n_ops": n_ops[op],
                    "tempos": tempos[op],
                    "media": media(tempos[op]),
                    "desvio": desvio_padrao(tempos[op]),
                    "comparacoes": comparacoes.get(op),
                    "digest": digests[op],
                }

    return resultados


# ---------------------------------------------------------------- ambiente

def descobrir_ambiente():
    """Melhor esforco. Se algum campo vier 'n/d', preencha a mao no relatorio."""
    info = {
        "sistema_operacional": platform.platform(),
        "python": platform.python_version() + " (" + platform.python_implementation() + ")",
        "processador": platform.processor() or "n/d",
        "nucleos_logicos": os.cpu_count(),
        "memoria_gb": None,
    }

    try:
        with open("/proc/cpuinfo", encoding="utf-8") as arquivo:
            for linha in arquivo:
                if linha.startswith("model name"):
                    info["processador"] = linha.split(":", 1)[1].strip()
                    break
        with open("/proc/meminfo", encoding="utf-8") as arquivo:
            for linha in arquivo:
                if linha.startswith("MemTotal"):
                    info["memoria_gb"] = round(int(linha.split()[1]) / 1024 / 1024, 1)
                    break
    except OSError:
        pass

    try:
        if sys.platform == "darwin":
            def sysctl(chave):
                return subprocess.run(["sysctl", "-n", chave], capture_output=True,
                                      text=True).stdout.strip()
            info["processador"] = sysctl("machdep.cpu.brand_string") or info["processador"]
            info["memoria_gb"] = round(int(sysctl("hw.memsize")) / 1024 ** 3, 1)

        elif sys.platform == "win32":
            import ctypes

            class EstadoMemoria(ctypes.Structure):
                _fields_ = [("tamanho", ctypes.c_ulong), ("uso", ctypes.c_ulong),
                            ("total_fisica", ctypes.c_ulonglong),
                            ("livre_fisica", ctypes.c_ulonglong),
                            ("total_paginacao", ctypes.c_ulonglong),
                            ("livre_paginacao", ctypes.c_ulonglong),
                            ("total_virtual", ctypes.c_ulonglong),
                            ("livre_virtual", ctypes.c_ulonglong),
                            ("livre_estendida", ctypes.c_ulonglong)]

            estado = EstadoMemoria()
            estado.tamanho = ctypes.sizeof(EstadoMemoria)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(estado))
            info["memoria_gb"] = round(estado.total_fisica / 1024 ** 3, 1)
    except Exception:
        pass

    if info["memoria_gb"] is None:
        info["memoria_gb"] = "n/d"

    return info


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--versao", choices=("base", "otimizada"), required=True)
    parser.add_argument("--saida", required=True)
    parser.add_argument("--tamanhos", type=int, nargs="+", default=[100, 1000, 5000, 10000])
    parser.add_argument("--repeticoes", type=int, default=5)
    parser.add_argument("--semente", type=int, default=42)
    parser.add_argument("--sem-contagem", action="store_true")
    argumentos = parser.parse_args()

    resultados = medir_versao(argumentos.versao, argumentos.tamanhos, argumentos.repeticoes,
                              argumentos.semente, not argumentos.sem_contagem)

    documento = {
        "versao": argumentos.versao,
        "ambiente": descobrir_ambiente(),
        "parametros": {
            "tamanhos": argumentos.tamanhos,
            "repeticoes": argumentos.repeticoes,
            "semente": argumentos.semente,
            "cenarios": list(gerar_dados.CENARIOS),
            "operacoes": list(OPERACOES),
        },
        "resultados": resultados,
    }

    with open(argumentos.saida, "w", encoding="utf-8") as arquivo:
        json.dump(documento, arquivo, ensure_ascii=False, indent=1)

    print(f"[{argumentos.versao}] salvo em {argumentos.saida}", flush=True)


if __name__ == "__main__":
    main()

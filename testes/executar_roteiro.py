"""Executa o main.main() (ou um script) de uma versao alimentando o input() com um roteiro.

uso: python executar_roteiro.py <pasta_da_versao> <arquivo_do_roteiro>
"""
import builtins
import sys

pasta = sys.argv[1]
roteiro = open(sys.argv[2], encoding="utf-8").read().split("\n")

sys.path.insert(0, pasta)
entradas = iter(roteiro)


def entrada_falsa(mensagem=""):
    try:
        valor = next(entradas)
    except StopIteration:
        raise SystemExit("[roteiro acabou antes do programa]")

    print(f"{mensagem}{valor}")
    return valor


builtins.input = entrada_falsa

import main

main.main()

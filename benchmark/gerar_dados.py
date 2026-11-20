"""Massa de dados reproduzivel (semente fixa), identica para as duas versoes.

Cenarios (valem para a ordem em que as ordens de servico chegam):
  aleatorio : codigos, prioridades e valores embaralhados          -> caso medio
  ordenado  : ja na ordem que os relatorios pedem                  -> melhor caso
              (codigos e valores crescentes, prioridades da maior para a menor)
  inverso   : na ordem contraria a dos relatorios                  -> pior caso
              (codigos e valores decrescentes, prioridades da menor para a maior)

Os codigos guardados sao sempre PARES (2, 4, 6...). Assim os IMPARES sao codigos
que nao existem, mas caem no meio da faixa (busca inexistente realista).
"""
import random

CENARIOS = ("aleatorio", "ordenado", "inverso")
MAX_CONSULTAS = 1000


def gerar_massa(n, cenario, semente=42):
    """Devolve n tuplas (codigo, cliente, veiculo, problema, prioridade, valor) na ordem de chegada."""
    rng = random.Random(f"massa-{semente}-{n}-{cenario}")
    codigos = [2 * c for c in range(1, n + 1)]

    if cenario == "aleatorio":
        rng.shuffle(codigos)
        prioridades = [rng.randint(1, 5) for _ in range(n)]
        valores = [round(rng.uniform(50, 5000), 2) for _ in range(n)]

    elif cenario == "ordenado":
        prioridades = [5 - (i * 5) // n for i in range(n)]
        valores = [round(50 + i * 0.5, 2) for i in range(n)]

    elif cenario == "inverso":
        codigos.reverse()
        prioridades = [1 + (i * 5) // n for i in range(n)]
        valores = [round(50 + (n - 1 - i) * 0.5, 2) for i in range(n)]

    else:
        raise ValueError(f"cenario desconhecido: {cenario}")

    massa = []
    for i in range(n):
        codigo = codigos[i]
        massa.append((codigo, f"Cliente {codigo}", f"Veiculo {codigo % 50}",
                      "Revisao geral", prioridades[i], valores[i]))

    return massa


def _quantidade(n):
    return n if n < MAX_CONSULTAS else MAX_CONSULTAS


def codigos_existentes(n, semente=42):
    """Codigos que estao cadastrados, em ordem aleatoria fixa."""
    rng = random.Random(f"existentes-{semente}-{n}")
    return [2 * c for c in rng.sample(range(1, n + 1), _quantidade(n))]


def codigos_inexistentes(n, semente=42):
    """Codigos (impares) que nao estao cadastrados."""
    rng = random.Random(f"inexistentes-{semente}-{n}")
    return [2 * c + 1 for c in rng.sample(range(0, n), _quantidade(n))]


def codigos_para_remover(n, semente=42):
    """Codigos cadastrados que serao removidos, em ordem aleatoria fixa."""
    rng = random.Random(f"remocao-{semente}-{n}")
    return [2 * c for c in rng.sample(range(1, n + 1), _quantidade(n))]

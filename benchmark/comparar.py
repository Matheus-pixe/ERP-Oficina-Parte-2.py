"""Mede a versao base e a otimizada na mesma maquina e gera as tabelas comparativas.

uso (a partir da raiz do repositorio):
    python benchmark/comparar.py
    python benchmark/comparar.py --tamanhos 100 1000 --repeticoes 5     (mais rapido)
    python benchmark/comparar.py --so-tabelas                           (refaz as tabelas dos JSON ja gerados)

Saidas em benchmark/resultados/ (ou na pasta de --saida):
    base.json, otimizada.json   dados brutos (todos os tempos de cada repeticao)
    comparativo.md              tabelas por operacao, ambiente e verificacao de equivalencia
    resultados.csv              tudo em uma planilha
"""
import argparse
import csv
import json
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))

ROTULOS = {
    "inserir": "Inserção (cadastro de n OS, com checagem de código repetido)",
    "busca_existente": "Busca de código existente",
    "busca_inexistente": "Busca de código inexistente",
    "relatorio_prioridade": "Relatório por prioridade (ordenação)",
    "relatorio_valor": "Relatório por valor (ordenação)",
    "listagem_por_codigo": "Listagem ordenada por código",
    "listagem_cadastro": "Listagem em ordem de cadastro (listar_ordens)",
    "remocao": "Remoção de OS (registro + fila)",
    "processar_fila": "Processar toda a fila de prioridade (n extrações)",
}

NOME_CENARIO = {
    "aleatorio": "aleatório (médio)",
    "ordenado": "ordenado (melhor)",
    "inverso": "inverso (pior)",
}


def tempo(segundos):
    if segundos >= 1:
        return f"{segundos:.3f} s"
    if segundos >= 1e-3:
        return f"{segundos * 1e3:.3f} ms"
    return f"{segundos * 1e6:.1f} µs"


def inteiro(valor):
    if valor is None:
        return "n/d"
    return f"{valor:,}".replace(",", ".")


def ganho(base, otimizada):
    if otimizada <= 0:
        return "n/d"
    razao = base / otimizada
    if razao >= 10:
        return f"{razao:.0f}×"
    return f"{razao:.2f}×"


def medir(versao, argumentos, arquivo):
    comando = [sys.executable, "-I", os.path.join(AQUI, "medir.py"),
               "--versao", versao, "--saida", arquivo,
               "--tamanhos", *[str(t) for t in argumentos.tamanhos],
               "--repeticoes", str(argumentos.repeticoes),
               "--semente", str(argumentos.semente)]
    if argumentos.sem_contagem:
        comando.append("--sem-contagem")
    subprocess.run(comando, check=True)


def tabelas(base, otim):
    tamanhos = base["parametros"]["tamanhos"]
    repeticoes = base["parametros"]["repeticoes"]
    ambiente = base["ambiente"]
    linhas = []
    divergencias = []
    conferidas = 0

    linhas.append("# Comparativo de desempenho: versão base × versão otimizada\n")
    linhas.append("## Ambiente\n")
    linhas.append(f"- Sistema operacional: {ambiente['sistema_operacional']}")
    linhas.append(f"- Processador: {ambiente['processador']} ({ambiente['nucleos_logicos']} núcleos lógicos)")
    linhas.append(f"- Memória: {ambiente['memoria_gb']} GB")
    linhas.append(f"- Python: {ambiente['python']}")
    if otim["ambiente"] != ambiente:
        linhas.append("- AVISO: as duas versões foram medidas em ambientes diferentes.")
    linhas.append("\n## Parâmetros\n")
    linhas.append(f"- Tamanhos: {', '.join(str(t) for t in tamanhos)} registros")
    linhas.append("- Cenários: aleatório (caso médio), ordenado (melhor caso), inverso (pior caso)")
    linhas.append(f"- Repetições: {repeticoes} por medição (mais 1 de aquecimento descartada); "
                  "valores = média ± desvio padrão amostral")
    linhas.append(f"- Semente da massa de dados: {base['parametros']['semente']} (idêntica nas duas versões)")
    linhas.append("- Comparações: número de comparações de chaves, contado em uma execução à parte")
    linhas.append("- Ganho = tempo da base ÷ tempo da otimizada (abaixo de 1× significa que a otimizada ficou mais lenta)\n")

    maior = str(tamanhos[-1])
    linhas.append(f"## Resumo: n = {maior}, cenário aleatório\n")
    linhas.append("| Operação | Base | Otimizada | Ganho |")
    linhas.append("|---|---|---|---|")
    for op, rotulo in ROTULOS.items():
        b = base["resultados"][maior]["aleatorio"][op]
        o = otim["resultados"][maior]["aleatorio"][op]
        linhas.append(f"| {rotulo} | {tempo(b['media'])} | {tempo(o['media'])} | "
                      f"{ganho(b['media'], o['media'])} |")

    for op, rotulo in ROTULOS.items():
        n_ops = base["resultados"][str(tamanhos[0])]["aleatorio"][op]["n_ops"]
        linhas.append(f"\n## {rotulo}\n")
        linhas.append("| n | Cenário | Base (média ± dp) | Otimizada (média ± dp) | Ganho | "
                      "Comparações base | Comparações otimizada | Resultado idêntico |")
        linhas.append("|---|---|---|---|---|---|---|---|")

        for n in tamanhos:
            for cenario in base["parametros"]["cenarios"]:
                b = base["resultados"][str(n)][cenario][op]
                o = otim["resultados"][str(n)][cenario][op]
                igual = b["digest"] == o["digest"]
                conferidas += 1
                if not igual:
                    divergencias.append(f"{op} n={n} {cenario}")
                linhas.append(
                    f"| {n} | {NOME_CENARIO[cenario]} | "
                    f"{tempo(b['media'])} ± {tempo(b['desvio'])} | "
                    f"{tempo(o['media'])} ± {tempo(o['desvio'])} | "
                    f"{ganho(b['media'], o['media'])} | "
                    f"{inteiro(b['comparacoes'])} | {inteiro(o['comparacoes'])} | "
                    f"{'sim' if igual else 'NÃO'} |")

        if op in ("busca_existente", "busca_inexistente", "remocao"):
            linhas.append(f"\nCada medição executa até {n_ops} operações (n = 100 usa 100); "
                          "o tempo da tabela é o total do conjunto.")
        elif op in ("inserir", "processar_fila"):
            linhas.append("\nCada medição executa n operações; o tempo da tabela é o total.")

    linhas.append("\n## Verificação de equivalência\n")
    if divergencias:
        linhas.append(f"**ATENÇÃO:** {len(divergencias)} de {conferidas} medições deram resultados "
                      "diferentes entre as versões:\n")
        for item in divergencias:
            linhas.append(f"- {item}")
    else:
        linhas.append(f"As {conferidas} medições (operações × tamanhos × cenários) produziram "
                      "resultados idênticos nas duas versões: mesmas ordens nos relatórios e "
                      "listagens, mesma ordem de saída da fila e mesmo estado após as remoções "
                      "(comparação por hash dos resultados).")

    return "\n".join(linhas) + "\n", divergencias


def gravar_csv(caminho, base, otim):
    with open(caminho, "w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(["versao", "tamanho", "cenario", "operacao", "n_operacoes",
                           "media_s", "desvio_s", "comparacoes", "digest"])
        for nome, dados in (("base", base), ("otimizada", otim)):
            for n in dados["parametros"]["tamanhos"]:
                for cenario in dados["parametros"]["cenarios"]:
                    for op in ROTULOS:
                        r = dados["resultados"][str(n)][cenario][op]
                        escritor.writerow([nome, n, cenario, op, r["n_ops"], r["media"],
                                           r["desvio"], r["comparacoes"], r["digest"]])


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--tamanhos", type=int, nargs="+", default=[100, 1000, 5000, 10000])
    parser.add_argument("--repeticoes", type=int, default=5)
    parser.add_argument("--semente", type=int, default=42)
    parser.add_argument("--saida", default=os.path.join(AQUI, "resultados"))
    parser.add_argument("--sem-contagem", action="store_true")
    parser.add_argument("--so-tabelas", action="store_true")
    argumentos = parser.parse_args()

    os.makedirs(argumentos.saida, exist_ok=True)
    arquivo_base = os.path.join(argumentos.saida, "base.json")
    arquivo_otim = os.path.join(argumentos.saida, "otimizada.json")

    if not argumentos.so_tabelas:
        medir("base", argumentos, arquivo_base)
        medir("otimizada", argumentos, arquivo_otim)

    with open(arquivo_base, encoding="utf-8") as f:
        base = json.load(f)
    with open(arquivo_otim, encoding="utf-8") as f:
        otim = json.load(f)

    texto, divergencias = tabelas(base, otim)

    with open(os.path.join(argumentos.saida, "comparativo.md"), "w", encoding="utf-8") as f:
        f.write(texto)
    gravar_csv(os.path.join(argumentos.saida, "resultados.csv"), base, otim)

    print(f"\nTabelas em {os.path.join(argumentos.saida, 'comparativo.md')}")
    if divergencias:
        print(f"ATENCAO: {len(divergencias)} medicoes com resultados diferentes entre as versoes")
        sys.exit(1)
    print("Resultados identicos nas duas versoes em todas as medicoes.")


if __name__ == "__main__":
    main()

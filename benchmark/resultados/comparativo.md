# Comparativo de desempenho: versão base × versão otimizada

## Ambiente

- Sistema operacional: Linux-6.18.44-fc-v726-x86_64-with-glibc2.39
- Processador: Intel(R) Xeon(R) Processor @ 2.30GHz (2 núcleos lógicos)
- Memória: 7.8 GB
- Python: 3.13.18 (CPython)

## Parâmetros

- Tamanhos: 100, 1000, 5000, 10000 registros
- Cenários: aleatório (caso médio), ordenado (melhor caso), inverso (pior caso)
- Repetições: 5 por medição (mais 1 de aquecimento descartada); valores = média ± desvio padrão amostral
- Semente da massa de dados: 42 (idêntica nas duas versões)
- Comparações: número de comparações de chaves, contado em uma execução à parte
- Ganho = tempo da base ÷ tempo da otimizada (abaixo de 1× significa que a otimizada ficou mais lenta)

## Resumo: n = 10000, cenário aleatório

| Operação | Base | Otimizada | Ganho |
|---|---|---|---|
| Inserção (cadastro de n OS, com checagem de código repetido) | 1.330 s | 47.316 ms | 28× |
| Busca de código existente | 136.222 ms | 779.8 µs | 175× |
| Busca de código inexistente | 281.883 ms | 881.9 µs | 320× |
| Relatório por prioridade (ordenação) | 2.922 s | 28.111 ms | 104× |
| Relatório por valor (ordenação) | 3.702 s | 27.738 ms | 133× |
| Listagem ordenada por código | 3.598 s | 1.573 ms | 2288× |
| Listagem em ordem de cadastro (listar_ordens) | 40.8 µs | 24.297 ms | 0.00× |
| Remoção de OS (registro + fila) | 284.232 ms | 6.257 ms | 45× |
| Processar toda a fila de prioridade (n extrações) | 1.810 s | 52.650 ms | 34× |

## Inserção (cadastro de n OS, com checagem de código repetido)

| n | Cenário | Base (média ± dp) | Otimizada (média ± dp) | Ganho | Comparações base | Comparações otimizada | Resultado idêntico |
|---|---|---|---|---|---|---|---|
| 100 | aleatório (médio) | 143.6 µs ± 17.3 µs | 279.3 µs ± 20.9 µs | 0.51× | 4.950 | 2.219 | sim |
| 100 | ordenado (melhor) | 132.3 µs ± 6.2 µs | 326.4 µs ± 49.0 µs | 0.41× | 4.950 | 2.490 | sim |
| 100 | inverso (pior) | 139.2 µs ± 21.4 µs | 334.4 µs ± 30.7 µs | 0.42× | 4.950 | 2.229 | sim |
| 1000 | aleatório (médio) | 12.405 ms ± 1.189 ms | 3.700 ms ± 233.4 µs | 3.35× | 499.500 | 34.102 | sim |
| 1000 | ordenado (melhor) | 15.192 ms ± 146.7 µs | 3.455 ms ± 172.4 µs | 4.40× | 499.500 | 37.906 | sim |
| 1000 | inverso (pior) | 12.592 ms ± 249.9 µs | 3.756 ms ± 167.7 µs | 3.35× | 499.500 | 31.911 | sim |
| 5000 | aleatório (médio) | 308.685 ms ± 32.673 ms | 21.128 ms ± 272.0 µs | 15× | 12.497.500 | 212.810 | sim |
| 5000 | ordenado (melhor) | 265.555 ms ± 4.680 ms | 20.969 ms ± 1.913 ms | 13× | 12.497.500 | 237.234 | sim |
| 5000 | inverso (pior) | 276.289 ms ± 15.196 ms | 21.308 ms ± 105.8 µs | 13× | 12.497.500 | 195.031 | sim |
| 10000 | aleatório (médio) | 1.330 s ± 198.979 ms | 47.316 ms ± 5.321 ms | 28× | 49.995.000 | 459.410 | sim |
| 10000 | ordenado (melhor) | 1.158 s ± 99.918 ms | 42.794 ms ± 1.500 ms | 27× | 49.995.000 | 514.466 | sim |
| 10000 | inverso (pior) | 1.191 s ± 169.681 ms | 45.663 ms ± 400.7 µs | 26× | 49.995.000 | 419.899 | sim |

Cada medição executa n operações; o tempo da tabela é o total.

## Busca de código existente

| n | Cenário | Base (média ± dp) | Otimizada (média ± dp) | Ganho | Comparações base | Comparações otimizada | Resultado idêntico |
|---|---|---|---|---|---|---|---|
| 100 | aleatório (médio) | 125.9 µs ± 7.3 µs | 33.9 µs ± 2.3 µs | 3.71× | 5.050 | 1.072 | sim |
| 100 | ordenado (melhor) | 130.3 µs ± 13.8 µs | 30.0 µs ± 0.5 µs | 4.33× | 5.050 | 1.060 | sim |
| 100 | inverso (pior) | 129.0 µs ± 16.4 µs | 32.1 µs ± 1.8 µs | 4.02× | 5.050 | 1.060 | sim |
| 1000 | aleatório (médio) | 12.697 ms ± 1.467 ms | 464.5 µs ± 31.5 µs | 27× | 500.500 | 17.392 | sim |
| 1000 | ordenado (melhor) | 15.283 ms ± 570.7 µs | 448.2 µs ± 56.5 µs | 34× | 500.500 | 16.974 | sim |
| 1000 | inverso (pior) | 12.592 ms ± 364.2 µs | 453.7 µs ± 28.3 µs | 28× | 500.500 | 16.974 | sim |
| 5000 | aleatório (médio) | 61.957 ms ± 5.645 ms | 862.2 µs ± 70.1 µs | 72× | 2.553.805 | 22.160 | sim |
| 5000 | ordenado (melhor) | 52.643 ms ± 758.1 µs | 693.5 µs ± 79.5 µs | 76× | 2.488.309 | 21.784 | sim |
| 5000 | inverso (pior) | 57.918 ms ± 8.863 ms | 559.5 µs ± 29.7 µs | 104× | 2.512.691 | 21.750 | sim |
| 10000 | aleatório (médio) | 136.222 ms ± 36.852 ms | 779.8 µs ± 72.3 µs | 175× | 5.034.074 | 24.094 | sim |
| 10000 | ordenado (melhor) | 122.923 ms ± 28.094 ms | 675.0 µs ± 35.1 µs | 182× | 4.803.379 | 23.708 | sim |
| 10000 | inverso (pior) | 128.433 ms ± 25.525 ms | 613.9 µs ± 11.5 µs | 209× | 5.197.621 | 23.818 | sim |

Cada medição executa até 100 operações (n = 100 usa 100); o tempo da tabela é o total do conjunto.

## Busca de código inexistente

| n | Cenário | Base (média ± dp) | Otimizada (média ± dp) | Ganho | Comparações base | Comparações otimizada | Resultado idêntico |
|---|---|---|---|---|---|---|---|
| 100 | aleatório (médio) | 247.0 µs ± 56.3 µs | 49.3 µs ± 21.0 µs | 5.01× | 10.000 | 1.358 | sim |
| 100 | ordenado (melhor) | 231.6 µs ± 16.0 µs | 38.1 µs ± 3.3 µs | 6.08× | 10.000 | 1.346 | sim |
| 100 | inverso (pior) | 214.6 µs ± 18.5 µs | 37.6 µs ± 1.4 µs | 5.72× | 10.000 | 1.346 | sim |
| 1000 | aleatório (médio) | 25.775 ms ± 3.012 ms | 451.4 µs ± 33.6 µs | 57× | 1.000.000 | 20.374 | sim |
| 1000 | ordenado (melhor) | 32.422 ms ± 1.112 ms | 481.7 µs ± 40.1 µs | 67× | 1.000.000 | 19.954 | sim |
| 1000 | inverso (pior) | 25.885 ms ± 326.1 µs | 457.7 µs ± 39.0 µs | 57× | 1.000.000 | 19.954 | sim |
| 5000 | aleatório (médio) | 118.460 ms ± 5.556 ms | 843.9 µs ± 112.7 µs | 140× | 5.000.000 | 25.074 | sim |
| 5000 | ordenado (melhor) | 108.243 ms ± 9.654 ms | 676.4 µs ± 85.5 µs | 160× | 5.000.000 | 24.728 | sim |
| 5000 | inverso (pior) | 125.109 ms ± 24.265 ms | 628.5 µs ± 36.1 µs | 199× | 5.000.000 | 24.720 | sim |
| 10000 | aleatório (médio) | 281.883 ms ± 43.444 ms | 881.9 µs ± 124.1 µs | 320× | 10.000.000 | 27.146 | sim |
| 10000 | ordenado (melhor) | 261.191 ms ± 55.618 ms | 749.8 µs ± 103.9 µs | 348× | 10.000.000 | 26.786 | sim |
| 10000 | inverso (pior) | 232.775 ms ± 28.040 ms | 651.1 µs ± 21.4 µs | 357× | 10.000.000 | 26.668 | sim |

Cada medição executa até 100 operações (n = 100 usa 100); o tempo da tabela é o total do conjunto.

## Relatório por prioridade (ordenação)

| n | Cenário | Base (média ± dp) | Otimizada (média ± dp) | Ganho | Comparações base | Comparações otimizada | Resultado idêntico |
|---|---|---|---|---|---|---|---|
| 100 | aleatório (médio) | 263.8 µs ± 12.3 µs | 152.3 µs ± 19.8 µs | 1.73× | 4.950 | 1.096 | sim |
| 100 | ordenado (melhor) | 175.1 µs ± 14.6 µs | 132.9 µs ± 5.1 µs | 1.32× | 4.950 | 632 | sim |
| 100 | inverso (pior) | 326.2 µs ± 49.5 µs | 172.0 µs ± 42.6 µs | 1.90× | 4.950 | 854 | sim |
| 1000 | aleatório (médio) | 27.414 ms ± 4.187 ms | 2.221 ms ± 32.1 µs | 12× | 499.500 | 17.396 | sim |
| 1000 | ordenado (melhor) | 23.701 ms ± 706.7 µs | 1.495 ms ± 101.9 µs | 16× | 499.500 | 9.864 | sim |
| 1000 | inverso (pior) | 37.593 ms ± 1.059 ms | 1.676 ms ± 120.2 µs | 22× | 499.500 | 11.678 | sim |
| 5000 | aleatório (médio) | 696.860 ms ± 22.460 ms | 12.808 ms ± 207.0 µs | 54× | 12.497.500 | 110.498 | sim |
| 5000 | ordenado (melhor) | 432.991 ms ± 45.056 ms | 8.678 ms ± 332.4 µs | 50× | 12.497.500 | 59.608 | sim |
| 5000 | inverso (pior) | 832.534 ms ± 46.079 ms | 9.685 ms ± 979.0 µs | 86× | 12.497.500 | 71.996 | sim |
| 10000 | aleatório (médio) | 2.922 s ± 187.462 ms | 28.111 ms ± 1.057 ms | 104× | 49.995.000 | 240.958 | sim |
| 10000 | ordenado (melhor) | 1.837 s ± 188.001 ms | 19.560 ms ± 4.256 ms | 94× | 49.995.000 | 129.216 | sim |
| 10000 | inverso (pior) | 3.641 s ± 369.353 ms | 19.777 ms ± 411.4 µs | 184× | 49.995.000 | 154.004 | sim |

## Relatório por valor (ordenação)

| n | Cenário | Base (média ± dp) | Otimizada (média ± dp) | Ganho | Comparações base | Comparações otimizada | Resultado idêntico |
|---|---|---|---|---|---|---|---|
| 100 | aleatório (médio) | 274.5 µs ± 24.6 µs | 161.1 µs ± 50.5 µs | 1.70× | 4.950 | 1.104 | sim |
| 100 | ordenado (melhor) | 179.7 µs ± 11.3 µs | 136.6 µs ± 23.4 µs | 1.32× | 4.950 | 632 | sim |
| 100 | inverso (pior) | 325.4 µs ± 42.2 µs | 134.9 µs ± 17.3 µs | 2.41× | 4.950 | 632 | sim |
| 1000 | aleatório (médio) | 29.720 ms ± 2.902 ms | 2.109 ms ± 125.5 µs | 14× | 499.500 | 17.436 | sim |
| 1000 | ordenado (melhor) | 23.747 ms ± 796.6 µs | 1.456 ms ± 101.9 µs | 16× | 499.500 | 9.864 | sim |
| 1000 | inverso (pior) | 41.671 ms ± 1.042 ms | 1.500 ms ± 64.8 µs | 28× | 499.500 | 9.864 | sim |
| 5000 | aleatório (médio) | 853.633 ms ± 117.199 ms | 12.363 ms ± 367.1 µs | 69× | 12.497.500 | 110.510 | sim |
| 5000 | ordenado (melhor) | 415.272 ms ± 5.258 ms | 8.684 ms ± 1.109 ms | 48× | 12.497.500 | 59.608 | sim |
| 5000 | inverso (pior) | 966.310 ms ± 53.095 ms | 7.729 ms ± 94.1 µs | 125× | 12.497.500 | 59.608 | sim |
| 10000 | aleatório (médio) | 3.702 s ± 200.637 ms | 27.738 ms ± 3.703 ms | 133× | 49.995.000 | 240.988 | sim |
| 10000 | ordenado (melhor) | 1.962 s ± 297.537 ms | 18.070 ms ± 2.380 ms | 109× | 49.995.000 | 129.216 | sim |
| 10000 | inverso (pior) | 4.103 s ± 250.301 ms | 17.362 ms ± 397.7 µs | 236× | 49.995.000 | 129.216 | sim |

## Listagem ordenada por código

| n | Cenário | Base (média ± dp) | Otimizada (média ± dp) | Ganho | Comparações base | Comparações otimizada | Resultado idêntico |
|---|---|---|---|---|---|---|---|
| 100 | aleatório (médio) | 306.9 µs ± 27.9 µs | 21.1 µs ± 2.0 µs | 15× | 4.950 | 0 | sim |
| 100 | ordenado (melhor) | 179.3 µs ± 16.0 µs | 21.4 µs ± 0.1 µs | 8.39× | 4.950 | 0 | sim |
| 100 | inverso (pior) | 394.5 µs ± 82.7 µs | 19.7 µs ± 1.5 µs | 20× | 4.950 | 0 | sim |
| 1000 | aleatório (médio) | 28.560 ms ± 1.160 ms | 131.5 µs ± 17.8 µs | 217× | 499.500 | 0 | sim |
| 1000 | ordenado (melhor) | 23.503 ms ± 595.8 µs | 116.5 µs ± 5.1 µs | 202× | 499.500 | 0 | sim |
| 1000 | inverso (pior) | 41.240 ms ± 1.643 ms | 128.0 µs ± 28.6 µs | 322× | 499.500 | 0 | sim |
| 5000 | aleatório (médio) | 830.365 ms ± 47.398 ms | 869.3 µs ± 78.5 µs | 955× | 12.497.500 | 0 | sim |
| 5000 | ordenado (melhor) | 418.392 ms ± 31.035 ms | 640.6 µs ± 70.6 µs | 653× | 12.497.500 | 0 | sim |
| 5000 | inverso (pior) | 992.444 ms ± 155.158 ms | 531.8 µs ± 35.8 µs | 1866× | 12.497.500 | 0 | sim |
| 10000 | aleatório (médio) | 3.598 s ± 425.495 ms | 1.573 ms ± 259.4 µs | 2288× | 49.995.000 | 0 | sim |
| 10000 | ordenado (melhor) | 1.832 s ± 183.891 ms | 1.213 ms ± 177.8 µs | 1510× | 49.995.000 | 0 | sim |
| 10000 | inverso (pior) | 4.050 s ± 432.902 ms | 1.144 ms ± 144.2 µs | 3538× | 49.995.000 | 0 | sim |

## Listagem em ordem de cadastro (listar_ordens)

| n | Cenário | Base (média ± dp) | Otimizada (média ± dp) | Ganho | Comparações base | Comparações otimizada | Resultado idêntico |
|---|---|---|---|---|---|---|---|
| 100 | aleatório (médio) | 2.0 µs ± 0.4 µs | 143.8 µs ± 57.8 µs | 0.01× | 0 | 547 | sim |
| 100 | ordenado (melhor) | 1.8 µs ± 0.1 µs | 119.1 µs ± 17.0 µs | 0.02× | 0 | 316 | sim |
| 100 | inverso (pior) | 1.7 µs ± 0.1 µs | 128.5 µs ± 18.0 µs | 0.01× | 0 | 356 | sim |
| 1000 | aleatório (médio) | 3.6 µs ± 0.5 µs | 1.777 ms ± 110.2 µs | 0.00× | 0 | 8.711 | sim |
| 1000 | ordenado (melhor) | 12.0 µs ± 16.9 µs | 1.223 ms ± 67.9 µs | 0.01× | 0 | 4.932 | sim |
| 1000 | inverso (pior) | 15.0 µs ± 21.9 µs | 1.345 ms ± 84.8 µs | 0.01× | 0 | 5.044 | sim |
| 5000 | aleatório (médio) | 22.8 µs ± 19.7 µs | 10.418 ms ± 153.2 µs | 0.00× | 0 | 55.227 | sim |
| 5000 | ordenado (melhor) | 17.8 µs ± 4.6 µs | 7.475 ms ± 356.7 µs | 0.00× | 0 | 29.804 | sim |
| 5000 | inverso (pior) | 16.0 µs ± 3.6 µs | 7.306 ms ± 182.7 µs | 0.00× | 0 | 32.004 | sim |
| 10000 | aleatório (médio) | 40.8 µs ± 22.3 µs | 24.297 ms ± 5.342 ms | 0.00× | 0 | 120.382 | sim |
| 10000 | ordenado (melhor) | 33.6 µs ± 4.5 µs | 14.724 ms ± 342.7 µs | 0.00× | 0 | 64.608 | sim |
| 10000 | inverso (pior) | 32.6 µs ± 5.4 µs | 17.248 ms ± 3.645 ms | 0.00× | 0 | 69.008 | sim |

## Remoção de OS (registro + fila)

| n | Cenário | Base (média ± dp) | Otimizada (média ± dp) | Ganho | Comparações base | Comparações otimizada | Resultado idêntico |
|---|---|---|---|---|---|---|---|
| 100 | aleatório (médio) | 166.9 µs ± 3.4 µs | 263.6 µs ± 49.0 µs | 0.63× | 5.146 | 2.172 | sim |
| 100 | ordenado (melhor) | 172.8 µs ± 10.7 µs | 293.2 µs ± 36.9 µs | 0.59× | 5.334 | 2.006 | sim |
| 100 | inverso (pior) | 162.5 µs ± 30.2 µs | 281.8 µs ± 27.9 µs | 0.58× | 4.966 | 2.139 | sim |
| 1000 | aleatório (médio) | 12.829 ms ± 159.3 µs | 3.807 ms ± 239.9 µs | 3.37× | 503.108 | 32.498 | sim |
| 1000 | ordenado (melhor) | 15.075 ms ± 2.002 ms | 3.767 ms ± 235.6 µs | 4.00× | 516.244 | 32.511 | sim |
| 1000 | inverso (pior) | 12.315 ms ± 733.5 µs | 3.908 ms ± 192.1 µs | 3.15× | 486.756 | 33.232 | sim |
| 5000 | aleatório (médio) | 110.168 ms ± 3.584 ms | 5.886 ms ± 247.9 µs | 19× | 4.387.404 | 46.024 | sim |
| 5000 | ordenado (melhor) | 101.401 ms ± 14.529 ms | 5.325 ms ± 293.5 µs | 19× | 4.286.258 | 45.137 | sim |
| 5000 | inverso (pior) | 120.887 ms ± 27.484 ms | 5.139 ms ± 205.3 µs | 24× | 4.716.742 | 47.180 | sim |
| 10000 | aleatório (médio) | 284.232 ms ± 72.750 ms | 6.257 ms ± 1.173 ms | 45× | 9.409.752 | 49.593 | sim |
| 10000 | ordenado (melhor) | 225.135 ms ± 3.738 ms | 5.514 ms ± 360.3 µs | 41× | 9.710.368 | 48.684 | sim |
| 10000 | inverso (pior) | 217.125 ms ± 6.256 ms | 6.327 ms ± 1.308 ms | 34× | 9.292.632 | 51.588 | sim |

Cada medição executa até 100 operações (n = 100 usa 100); o tempo da tabela é o total do conjunto.

## Processar toda a fila de prioridade (n extrações)

| n | Cenário | Base (média ± dp) | Otimizada (média ± dp) | Ganho | Comparações base | Comparações otimizada | Resultado idêntico |
|---|---|---|---|---|---|---|---|
| 100 | aleatório (médio) | 207.2 µs ± 11.2 µs | 197.6 µs ± 31.3 µs | 1.05× | 4.950 | 1.704 | sim |
| 100 | ordenado (melhor) | 199.1 µs ± 6.2 µs | 231.1 µs ± 14.4 µs | 0.86× | 4.950 | 1.690 | sim |
| 100 | inverso (pior) | 188.2 µs ± 22.6 µs | 225.8 µs ± 21.7 µs | 0.83× | 4.950 | 1.676 | sim |
| 1000 | aleatório (médio) | 15.122 ms ± 860.4 µs | 3.736 ms ± 253.5 µs | 4.05× | 499.500 | 30.074 | sim |
| 1000 | ordenado (melhor) | 21.245 ms ± 2.296 ms | 3.682 ms ± 160.3 µs | 5.77× | 499.500 | 29.932 | sim |
| 1000 | inverso (pior) | 17.658 ms ± 1.066 ms | 3.585 ms ± 192.1 µs | 4.93× | 499.500 | 29.562 | sim |
| 5000 | aleatório (médio) | 403.033 ms ± 67.323 ms | 23.312 ms ± 210.8 µs | 17× | 12.497.500 | 196.416 | sim |
| 5000 | ordenado (melhor) | 397.476 ms ± 57.805 ms | 23.196 ms ± 677.2 µs | 17× | 12.497.500 | 196.456 | sim |
| 5000 | inverso (pior) | 417.312 ms ± 35.311 ms | 23.002 ms ± 990.7 µs | 18× | 12.497.500 | 196.128 | sim |
| 10000 | aleatório (médio) | 1.810 s ± 145.381 ms | 52.650 ms ± 4.683 ms | 34× | 49.995.000 | 432.862 | sim |
| 10000 | ordenado (melhor) | 1.662 s ± 132.849 ms | 50.065 ms ± 601.4 µs | 33× | 49.995.000 | 433.366 | sim |
| 10000 | inverso (pior) | 1.660 s ± 110.671 ms | 49.261 ms ± 377.9 µs | 34× | 49.995.000 | 433.036 | sim |

Cada medição executa n operações; o tempo da tabela é o total.

## Verificação de equivalência

As 108 medições (operações × tamanhos × cenários) produziram resultados idênticos nas duas versões: mesmas ordens nos relatórios e listagens, mesma ordem de saída da fila e mesmo estado após as remoções (comparação por hash dos resultados).

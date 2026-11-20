# ERP Oficina – Parte 1 (base) e Parte 2 (otimizada)

Repositório com as duas versões do sistema, para comparação de desempenho.

* `versao_base/` – entrega da Parte 1, congelada e sem alterações
* `versao_otimizada/` – AVL, travessias, Merge Sort e fila de prioridade com heap binário
* `benchmark/` – medições e tabelas comparativas
* `testes/` – testes automáticos
* `ALTERACOES.md` – o que foi acrescentado e retirado, e por que o heap foi a otimização adicional

## Executar o sistema

```
cd versao_base        # ou versao_otimizada
python main.py
```

Na versão otimizada, o menu de Ordens de Serviço ganhou as opções 11 (em ordem), 12 (pré-ordem) e 13 (pós-ordem).

## Testes

```
python testes/testes_otimizacoes.py
```

## Benchmark

```
python benchmark/comparar.py                       # 100, 1000, 5000 e 10000 registros, 5 repetições
python benchmark/comparar.py --tamanhos 100 1000   # versão rápida
```

Gera `benchmark/resultados/comparativo.md` (tabelas), `resultados.csv` e os JSON brutos. Massa de dados com semente fixa (42), idêntica nas duas versões; cenários aleatório, ordenado e inverso. O tamanho 10.000 leva cerca de 10 minutos por causa do Bubble Sort da base.

Requer apenas Python 3 (biblioteca padrão).

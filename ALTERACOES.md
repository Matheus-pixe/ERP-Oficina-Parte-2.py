# Parte 2 – O que foi acrescentado e o que foi retirado

Regra seguida: **nenhum nome de variável, função, classe ou arquivo existente foi renomeado**. A versão otimizada só ganhou código novo e teve trocadas as chamadas que dependiam da lista.

## Estrutura do repositório

| Pasta | Conteúdo |
|---|---|
| `versao_base/` | Parte 1 congelada, **sem nenhuma alteração** (cópia exata do repositório original) |
| `versao_otimizada/` | Parte 1 + otimizações da Parte 2 |
| `benchmark/` | Medição de desempenho (`comparar.py` roda tudo) e `resultados/` com os dados já gerados |
| `testes/` | 20 testes automáticos (AVL, heap, Merge Sort e equivalência entre as versões) |

> Sugestão de tag no Git: `git tag parte1-base` no commit que contém `versao_base/` antes de qualquer outra mudança, para cumprir o item 5.1.

## Otimizações

| # | Otimização | Onde | Substitui |
|---|---|---|---|
| 1 | **Árvore AVL** manual (inserir, remover, buscar, balancear, rotações simples e duplas) | `estruturas/arvore_avl.py` (novo) | lista `ordens` de `dados/ordens.py` + busca linear |
| 2 | **Travessias** em ordem, pré-ordem e pós-ordem | métodos da AVL + opções 11, 12 e 13 no menu de Ordens | – (funcionalidade nova) |
| 3 | **Merge Sort** manual, estável | `algoritmos/ordenacao.py` | Bubble Sort (usado nos relatórios por prioridade, valor e código) |
| 4 | **Otimização adicional: fila de prioridade com heap binário** | `estruturas/fila_prioridade.py` | varredura linear a cada extração |

### Por que o heap binário foi a otimização adicional

Analisando o código da Parte 1 (e confirmado nas medições), os gargalos que sobravam depois da AVL e do Merge Sort eram:

* `FilaPrioridade.remover_maior_prioridade` percorre a fila inteira a cada extração: **O(n)** por OS processada, **O(n²)** para esvaziar a fila (n = 10.000 → 1,81 s; com heap, 52 ms: **34×**).
* `remover_por_codigo` também varre a fila inteira ao remover uma OS.
* A fila é parte central do sistema (opção 8, "processar próxima OS"), diferente de cache ou tabela hash, que o sistema não precisaria.

Alternativas descartadas: **busca binária** (a AVL já resolve a busca por código), **tabela hash** (a restrição proíbe substituir a estrutura declarada por dicionário, e a AVL já cobre a busca) e **cache** (o sistema não repete consultas o bastante para compensar).

O heap mantém o **mesmo desempate da base**: entre prioridades iguais sai quem foi cadastrado primeiro. Isso é garantido pelo atributo novo `chegada`.

## Acrescentado

**Arquivos novos**
* `versao_otimizada/estruturas/arvore_avl.py` (classes `No` e `ArvoreAVL`)
* `benchmark/` (`gerar_dados.py`, `medir.py`, `comparar.py`, `resultados/`)
* `testes/` (`testes_otimizacoes.py`, `roteiros.py`, `executar_roteiro.py`)

**`models/ordem_servico.py`** – dois atributos novos na `OrdemServico`: `chegada` (número de ordem de cadastro, via contador de classe `proximo_chegada`) e `pos_fila` (posição da OS dentro do heap, `-1` se não estiver na fila).

**`estruturas/fila_prioridade.py`** – métodos novos: `_tem_precedencia`, `_trocar`, `_subir`, `_descer`, `_remover_na_posicao`, `remover(ordem)` (O(log n)) e `atualizar_prioridade(ordem)`. Os métodos `inserir`, `esta_vazia`, `remover_maior_prioridade`, `tamanho` e `remover_por_codigo` **mantêm nome e assinatura**; só o corpo mudou.

**`algoritmos/ordenacao.py`** – funções novas: `mesclar`, `merge_sort`, `prioridade_deve_trocar`, `valor_deve_trocar`, `codigo_deve_trocar`, `chegada_deve_trocar` e `ordenar_por_chegada`.

**`services/ordem_service.py`** – funções novas: `mostrar_travessia`, `exibir_em_ordem`, `exibir_pre_ordem`, `exibir_pos_ordem`.

**`main.py`** – três itens novos no menu de Ordens: `11` em ordem, `12` pré-ordem (com recuo por nível) e `13` pós-ordem.

## Retirado / substituído

* `dados/ordens.py`: `ordens = []` virou `ordens = ArvoreAVL()` (mesmo nome).
* `ordenacao.py`: o corpo dos dois laços aninhados do Bubble Sort em `ordenar_por_prioridade`, `ordenar_por_valor` e `ordenar_por_codigo` foi trocado por chamadas ao `merge_sort`. **Os nomes das três funções continuam iguais.**
* `fila_prioridade.py`: a varredura linear em `remover_maior_prioridade` foi trocada pelo heap.
* `ordem_service.py`: removidos o `import` de `buscar_ordem_por_codigo` e o `import` de `busca_binaria_ordem`, que deixaram de ser usados (as funções continuam existindo em `algoritmos/busca.py`, sem alteração). As chamadas `buscar_ordem_por_codigo(ordens, codigo)` / `ordens[indice]` / `ordens.append` / `ordens.pop` viraram `ordens.buscar` / `ordens.inserir` / `ordens.remover`. Nessas funções, a variável `indice` deixou de existir; no lugar dela, usa-se `ordem`.
* `alterar_prioridade` agora também chama `fila_ordens.atualizar_prioridade(ordem)` (necessário para o heap continuar correto).

**Não foram alterados:** `pecas.py`, `Parte_Rani.py`, `teste.py`, `busca.py`, `models/__init__.py` e os demais.

## Como o sistema continua igual

* Teste automático roda a mesma sessão completa (ordens, clientes, veículos, peças, histórico, relatórios, fila) nas duas versões: a saída é **idêntica**, exceto pelas 3 linhas novas do menu.
* O benchmark compara por hash o resultado de cada operação em todos os tamanhos e cenários: **0 divergências**.
* `teste.py` da Parte 1 roda igual nas duas.

## Pontos para conferir antes de entregar

1. **Erros da Parte 1:** rodei uma sessão completa na base (cadastro, duplicados, prioridades inválidas, serviços, remoção, fila vazia, clientes, veículos, peças) e **não encontrei erro que interrompa o programa**, por isso a base ficou intocada. Se o grupo conhecer algum bug, corrija-o em `versao_base/` **antes** de rodar o benchmark e registre no relatório.
2. **Há um custo:** com 100 registros a otimizada é mais lenta em inserção e remoção (constante maior da AVL e do heap), e a listagem em ordem de cadastro (`listar_ordens`) ficou mais lenta em todos os tamanhos, porque agora precisa reordenar por `chegada`. Isso deve entrar no relatório como análise honesta. Os ganhos aparecem a partir de ~1.000 registros.
3. **Ambiente:** os números de `benchmark/resultados/` foram medidos numa máquina de nuvem (2 núcleos, Python 3.13). Para o relatório, **rode `python benchmark/comparar.py` no computador do grupo** e use essas tabelas (o script já registra processador, memória, SO e versão do Python).
4. Comparações de chaves são contadas com tipos `int`/`float` instrumentados dentro do `medir.py`, sem alterar o código das versões.

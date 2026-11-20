#Merge Sort (divisão e conquista) implementado manualmente: O(n log n) em qualquer caso
#é estável, então os empates mantêm a ordem de chegada, igual ao Bubble Sort da versão base

#junta duas listas já ordenadas
#deve_trocar(esq, dir) é True quando dir tem que vir antes de esq
def mesclar(esquerda, direita, deve_trocar):
    resultado = []
    i = 0
    j = 0

    while i < len(esquerda) and j < len(direita):
        if deve_trocar(esquerda[i], direita[j]):
            resultado.append(direita[j])
            j += 1
        else:
            resultado.append(esquerda[i])
            i += 1

    while i < len(esquerda):
        resultado.append(esquerda[i])
        i += 1

    while j < len(direita):
        resultado.append(direita[j])
        j += 1

    return resultado

#divide a lista ao meio, ordena cada metade e junta (devolve uma lista nova)
def merge_sort(lista, deve_trocar):
    if len(lista) <= 1:
        return lista.copy()

    meio = len(lista) // 2

    esquerda = merge_sort(lista[:meio], deve_trocar)
    direita = merge_sort(lista[meio:], deve_trocar)

    return mesclar(esquerda, direita, deve_trocar)

#maior prioridade primeiro; empate: quem chegou antes
def prioridade_deve_trocar(esq, dir):
    if esq.prioridade != dir.prioridade:
        return esq.prioridade < dir.prioridade

    return esq.chegada > dir.chegada

#menor valor primeiro; empate: quem chegou antes
def valor_deve_trocar(esq, dir):
    if esq.valor_total != dir.valor_total:
        return esq.valor_total > dir.valor_total

    return esq.chegada > dir.chegada

def codigo_deve_trocar(esq, dir):
    return esq.codigo > dir.codigo

def chegada_deve_trocar(esq, dir):
    return esq.chegada > dir.chegada

def ordenar_por_prioridade(ordens):
    return merge_sort(ordens, prioridade_deve_trocar)

def ordenar_por_valor(ordens):
    return merge_sort(ordens, valor_deve_trocar)

def ordenar_por_codigo(ordens):
    return merge_sort(ordens, codigo_deve_trocar)

#novo: devolve as ordens na ordem em que foram cadastradas
def ordenar_por_chegada(ordens):
    return merge_sort(ordens, chegada_deve_trocar)

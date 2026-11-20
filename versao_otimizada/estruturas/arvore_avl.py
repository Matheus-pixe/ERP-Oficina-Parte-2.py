#árvore AVL (balanceada) implementada manualmente
#cada nó guarda uma chave (código da OS) e um valor (a OrdemServico)
#complexidade: inserir, remover e buscar em O(log n), mesmo com dados já ordenados

class No:
    def __init__(self, chave, valor):
        self.chave = chave
        self.valor = valor
        self.esquerda = None
        self.direita = None
        self.altura = 1


class ArvoreAVL:
    def __init__(self):
        self.raiz = None
        self.quantidade = 0

    def __len__(self):
        return self.quantidade

    def esta_vazia(self):
        return self.raiz is None

    def altura(self):
        return self._altura(self.raiz)

    # ---------- auxiliares de balanceamento ----------

    def _altura(self, no):
        if no is None:
            return 0
        return no.altura

    def _atualizar_altura(self, no):
        altura_esquerda = self._altura(no.esquerda)
        altura_direita = self._altura(no.direita)

        if altura_esquerda > altura_direita:
            no.altura = 1 + altura_esquerda
        else:
            no.altura = 1 + altura_direita

    def _fator_balanceamento(self, no):
        if no is None:
            return 0

        return self._altura(no.esquerda) - self._altura(no.direita)

    # ---------- rotações ----------

    def _rotacao_direita(self, y):
        x = y.esquerda
        meio = x.direita

        x.direita = y
        y.esquerda = meio

        self._atualizar_altura(y)
        self._atualizar_altura(x)

        return x

    def _rotacao_esquerda(self, x):
        y = x.direita
        meio = y.esquerda

        y.esquerda = x
        x.direita = meio

        self._atualizar_altura(x)
        self._atualizar_altura(y)

        return y

    def _balancear(self, no):
        self._atualizar_altura(no)

        fator = self._fator_balanceamento(no)

        #pesado à esquerda
        if fator > 1:
            #caso esquerda-direita: rotação dupla
            if self._fator_balanceamento(no.esquerda) < 0:
                no.esquerda = self._rotacao_esquerda(no.esquerda)

            return self._rotacao_direita(no)

        #pesado à direita
        if fator < -1:
            #caso direita-esquerda: rotação dupla
            if self._fator_balanceamento(no.direita) > 0:
                no.direita = self._rotacao_direita(no.direita)

            return self._rotacao_esquerda(no)

        return no

    # ---------- inserção ----------

    def inserir(self, chave, valor):
        #devolve True se inseriu e False se a chave já existia
        self._inserido = False

        self.raiz = self._inserir(self.raiz, chave, valor)

        if self._inserido:
            self.quantidade += 1

        return self._inserido

    def _inserir(self, no, chave, valor):
        if no is None:
            self._inserido = True
            return No(chave, valor)

        if chave < no.chave:
            no.esquerda = self._inserir(no.esquerda, chave, valor)

        elif chave > no.chave:
            no.direita = self._inserir(no.direita, chave, valor)

        else:
            #chave repetida: não insere
            return no

        return self._balancear(no)

    # ---------- busca ----------

    def buscar(self, chave):
        #devolve o valor guardado na chave ou None se não existir
        atual = self.raiz

        while atual is not None:
            if chave == atual.chave:
                return atual.valor

            elif chave < atual.chave:
                atual = atual.esquerda

            else:
                atual = atual.direita

        return None

    # ---------- remoção ----------

    def remover(self, chave):
        #devolve o valor removido ou None se a chave não existia
        self._achou = False
        self._removido = None

        self.raiz = self._remover(self.raiz, chave)

        if self._achou:
            self.quantidade -= 1

        return self._removido

    def _remover(self, no, chave):
        if no is None:
            return None

        if chave < no.chave:
            no.esquerda = self._remover(no.esquerda, chave)

        elif chave > no.chave:
            no.direita = self._remover(no.direita, chave)

        else:
            self._achou = True
            self._removido = no.valor

            #zero ou um filho: o filho (ou None) ocupa o lugar do nó
            if no.esquerda is None:
                return no.direita

            if no.direita is None:
                return no.esquerda

            #dois filhos: o sucessor (menor da direita) ocupa o lugar do nó
            sucessor = self._menor_no(no.direita)
            no.chave = sucessor.chave
            no.valor = sucessor.valor
            no.direita = self._remover_menor(no.direita)

        return self._balancear(no)

    def _menor_no(self, no):
        while no.esquerda is not None:
            no = no.esquerda

        return no

    def _remover_menor(self, no):
        if no.esquerda is None:
            return no.direita

        no.esquerda = self._remover_menor(no.esquerda)

        return self._balancear(no)

    # ---------- travessias ----------
    #com_nivel=True devolve pares (nivel, valor); a raiz está no nível 0

    def em_ordem(self, com_nivel=False):
        #esquerda, raiz, direita: chaves crescentes
        resultado = []
        self._em_ordem(self.raiz, 0, resultado, com_nivel)
        return resultado

    def _em_ordem(self, no, nivel, resultado, com_nivel):
        if no is None:
            return

        self._em_ordem(no.esquerda, nivel + 1, resultado, com_nivel)
        self._guardar(no, nivel, resultado, com_nivel)
        self._em_ordem(no.direita, nivel + 1, resultado, com_nivel)

    def pre_ordem(self, com_nivel=False):
        #raiz, esquerda, direita: mostra a hierarquia a partir da raiz
        resultado = []
        self._pre_ordem(self.raiz, 0, resultado, com_nivel)
        return resultado

    def _pre_ordem(self, no, nivel, resultado, com_nivel):
        if no is None:
            return

        self._guardar(no, nivel, resultado, com_nivel)
        self._pre_ordem(no.esquerda, nivel + 1, resultado, com_nivel)
        self._pre_ordem(no.direita, nivel + 1, resultado, com_nivel)

    def pos_ordem(self, com_nivel=False):
        #esquerda, direita, raiz: os filhos aparecem antes do pai
        resultado = []
        self._pos_ordem(self.raiz, 0, resultado, com_nivel)
        return resultado

    def _pos_ordem(self, no, nivel, resultado, com_nivel):
        if no is None:
            return

        self._pos_ordem(no.esquerda, nivel + 1, resultado, com_nivel)
        self._pos_ordem(no.direita, nivel + 1, resultado, com_nivel)
        self._guardar(no, nivel, resultado, com_nivel)

    def _guardar(self, no, nivel, resultado, com_nivel):
        if com_nivel:
            resultado.append((nivel, no.valor))
        else:
            resultado.append(no.valor)

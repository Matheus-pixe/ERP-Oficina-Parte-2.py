#fila de prioridade implementada como heap binário (maior prioridade na raiz)
#self.fila continua sendo uma lista, mas agora ela guarda o heap:
#o filho de i está em 2*i+1 e 2*i+2, o pai está em (i-1)//2
#empate de prioridade: sai primeiro quem chegou antes (menor chegada), como na versão base
class FilaPrioridade:
    def __init__(self):
        self.fila = []

    #True se a ordem a deve sair antes da ordem b
    def _tem_precedencia(self, a, b):
        if a.prioridade != b.prioridade:
            return a.prioridade > b.prioridade

        return a.chegada < b.chegada

    def _trocar(self, i, j):
        self.fila[i], self.fila[j] = self.fila[j], self.fila[i]

        self.fila[i].pos_fila = i
        self.fila[j].pos_fila = j

    def _subir(self, i):
        while i > 0:
            pai = (i - 1) // 2

            if self._tem_precedencia(self.fila[i], self.fila[pai]):
                self._trocar(i, pai)
                i = pai
            else:
                break

    def _descer(self, i):
        n = len(self.fila)

        while True:
            esquerda = 2 * i + 1
            direita = 2 * i + 2
            maior = i

            if esquerda < n and self._tem_precedencia(self.fila[esquerda], self.fila[maior]):
                maior = esquerda

            if direita < n and self._tem_precedencia(self.fila[direita], self.fila[maior]):
                maior = direita

            if maior == i:
                break

            self._trocar(i, maior)
            i = maior

    def inserir(self, ordem):
        # Cada ordem guarda uma única posição e só pode integrar uma fila.
        if ordem.pos_fila != -1:
            return

        self.fila.append(ordem)
        ordem.pos_fila = len(self.fila) - 1

        self._subir(ordem.pos_fila)

    def esta_vazia(self):
        return len(self.fila) == 0

    def remover_maior_prioridade(self):
        if self.esta_vazia():
            return None

        return self._remover_na_posicao(0)

    def tamanho(self):
        return len(self.fila)

    #tira a ordem que está na posição i do heap e conserta o heap
    def _remover_na_posicao(self, i):
        ordem = self.fila[i]
        ultima = self.fila.pop()

        if i < len(self.fila):
            self.fila[i] = ultima
            ultima.pos_fila = i

            self._subir(i)
            self._descer(ultima.pos_fila)

        ordem.pos_fila = -1

        return ordem

    #mantida da versão base: procura pelo código, então é O(n)
    def remover_por_codigo(self, codigo):
        for i in range(len(self.fila)):
            if self.fila[i].codigo == codigo:
                self._remover_na_posicao(i)
                return True

        return False

    #novo: remove uma ordem já conhecida usando a posição guardada nela, O(log n)
    def remover(self, ordem):
        if not (0 <= ordem.pos_fila < len(self.fila)) or self.fila[ordem.pos_fila] is not ordem:
            return False

        self._remover_na_posicao(ordem.pos_fila)
        return True

    #novo: deve ser chamado depois de mudar a prioridade de uma ordem que está na fila
    def atualizar_prioridade(self, ordem):
        if not (0 <= ordem.pos_fila < len(self.fila)) or self.fila[ordem.pos_fila] is not ordem:
            return

        self._subir(ordem.pos_fila)
        self._descer(ordem.pos_fila)


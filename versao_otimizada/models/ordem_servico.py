
from decimal import Decimal, DecimalException


CENTAVO = Decimal("0.01")


def valor_em_reais(valor):
    try:
        numero = Decimal(str(valor))
        if not numero.is_finite() or numero < 0:
            raise ValueError("O valor deve ser finito e não negativo.")
        monetario = numero.quantize(CENTAVO)
    except DecimalException as erro:
        raise ValueError("Valor fora da precisão suportada.") from erro
    if numero != monetario:
        raise ValueError("O valor deve ser expresso em centavos inteiros.")
    return monetario


class OrdemServico:
    #contador global que numera a chegada de cada OS (desempate: quem chegou antes sai antes)
    proximo_chegada = 0

    def __init__(self, codigo, cliente, veiculo, problema, prioridade):
        self.codigo = codigo
        self.cliente = cliente
        self.veiculo = veiculo
        self.problema = problema
        self.prioridade = prioridade
        
        self.status = "Aguardando"
        self.servicos = []
        self.valor_total = Decimal("0.00")

        #ordem de chegada e posição dentro do heap da fila (-1 = não está na fila)
        OrdemServico.proximo_chegada += 1
        self.chegada = OrdemServico.proximo_chegada
        self.pos_fila = -1

    def alterar_status(self, novo_status):
        self.status = novo_status

    def alterar_prioridade(self, nova_prioridade):
        self.prioridade = nova_prioridade

    def adicionar_servico(self, descricao, valor):
        valor = valor_em_reais(valor)
        novo_total = valor_em_reais(self.valor_total + valor)
        servico = {
            "descricao": descricao,
            "valor": valor
        }

        self.servicos.append(servico)
        self.valor_total = novo_total

    def calcular_valor(self):
        total = Decimal("0.00")

        for servico in self.servicos:
            total = valor_em_reais(total + valor_em_reais(servico["valor"]))

        self.valor_total = total


#classe pra ordem de serviço, esudar mais dps
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
        self.valor_total = 0

        #ordem de chegada e posição dentro do heap da fila (-1 = não está na fila)
        OrdemServico.proximo_chegada += 1
        self.chegada = OrdemServico.proximo_chegada
        self.pos_fila = -1

    def alterar_status(self, novo_status):
        self.status = novo_status

    def alterar_prioridade(self, nova_prioridade):
        self.prioridade = nova_prioridade

    def adicionar_servico(self, descricao, valor):
        servico = {
            "descricao": descricao,
            "valor": valor
        }

        self.servicos.append(servico)
        self.calcular_valor()

    def calcular_valor(self):
        total = 0

        for servico in self.servicos:
            total += servico["valor"]

        self.valor_total = total
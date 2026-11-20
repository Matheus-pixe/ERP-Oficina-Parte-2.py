"""Roteiros de entrada (linhas digitadas) para exercitar o main.py das duas versoes."""


def ordens(travessias=False):
    L = ["3"]  # menu Ordens de Servico

    def cadastrar(cod, cli, vei, prob, pri):
        L.extend(["1", str(cod), cli, vei, prob, str(pri)])

    cadastrar(30, "Joao", "Civic", "Troca de oleo", 2)
    cadastrar(10, "Maria", "Onix", "Motor nao liga", 5)
    cadastrar(20, "Pedro", "Gol", "Freios", 4)
    cadastrar(15, "Ana", "Uno", "Revisao", 4)
    cadastrar(40, "Lia", "Fiesta", "Suspensao", 5)
    cadastrar(25, "Rui", "Palio", "Bateria", 4)
    L.extend(["1", "10"])                        # codigo duplicado
    cadastrar(99, "Teste", "Teste", "Teste", 9)  # prioridade invalida
    L.append("3")                                # listar (ordem de cadastro)
    L.extend(["2", "20"])                        # consultar existente
    L.extend(["2", "77"])                        # consultar inexistente
    L.extend(["4", "20", "2"])                   # status -> Em manutencao
    L.extend(["4", "20", "9"])                   # status invalido
    L.extend(["4", "77"])                        # status de inexistente
    L.extend(["5", "30", "5"])                   # prioridade 2 -> 5
    L.extend(["5", "30", "7"])                   # prioridade invalida
    L.extend(["6", "30", "Pastilha", "150,50"])
    L.extend(["6", "30", "Alinhamento", "80"])
    L.extend(["6", "10", "Motor", "1200.75"])
    L.extend(["6", "20", "Freio", "150,50"])     # mesmo valor da 30 (empate)
    L.extend(["6", "77"])                        # servico em inexistente
    L.append("9")                                # relatorio por prioridade
    L.append("10")                               # relatorio por valor
    L.append("8")                                # processar (empate prioridade 5)
    L.append("8")
    L.extend(["5", "15", "5"])                   # sobe 15 para 5 (esta na fila)
    L.append("8")
    L.append("8")
    L.extend(["7", "25"])                        # remove 25 (ainda na fila)
    L.extend(["7", "10"])                        # remove 10 (ja processada)
    L.extend(["7", "999"])                       # remove inexistente
    L.append("9")
    L.append("10")
    L.append("3")
    L.append("8")
    L.append("8")                                # fila vazia
    if travessias:
        L.extend(["11", "12", "13"])
    L.append("0")                                # voltar
    return L


def clientes_veiculos():
    L = ["1", "1"]
    L.extend(["1", "Carlos", "1", "bia", "1", "Carlos",
              "2", "3", "bia", "3", "zzz", "4", "bia", "Beatriz",
              "5", "Carlos", "5", "nadie", "6"])
    L.append("2")
    L.extend(["1", "beatriz", "abc1d23", "Gol", "1", "beatriz", "abc1d23",
              "1", "nadie", "2", "ABC1D23", "3", "abc1d23", "xyz9z99", "Polo",
              "4", "xyz9z99", "5"])
    L.append("0")
    return L


def pecas():
    L = ["2"]
    L.extend(["1", "Pneu", "10", "200", "1", "Bateria", "3", "350.5",
              "1", "", "2", "Pneu", "2", "Nada", "3", "Pneu", "15", "",
              "5", "Pneu", "5", "6", "Pneu", "2", "6", "Pneu", "100",
              "7", "8", "8", "8", "4", "Bateria", "s", "4", "Pneu", "n", "0"])
    return L


def completo(travessias=False):
    return ordens(travessias) + clientes_veiculos() + pecas() + ["0"]

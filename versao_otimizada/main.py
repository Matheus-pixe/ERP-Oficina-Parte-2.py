from Parte_Rani import menu_principal as menu_clientes_veiculos
from pecas import menu as menu_estoque
from services.ordem_service import (
    cadastrar_ordem,
    listar_ordens,
    consultar_ordem,
    alterar_status,
    alterar_prioridade,
    registrar_servico,
    remover_ordem,
    processar_proxima_ordem,
    relatorio_por_prioridade,
    relatorio_por_valor,
    exibir_em_ordem,
    exibir_pre_ordem,
    exibir_pos_ordem
)


def menu_ordens():
    while True:
        print("\n==============================")
        print("     ORDENS DE SERVIÇO")
        print("==============================")

        print("1 - Cadastrar ordem de serviço")
        print("2 - Consultar ordem de serviço")
        print("3 - Listar ordens")
        print("4 - Alterar status")
        print("5 - Alterar prioridade")
        print("6 - Registrar serviço")
        print("7 - Remover ordem")
        print("8 - Processar próxima ordem")
        print("9 - Relatório por prioridade")
        print("10 - Relatório por valor")
        print("11 - Exibir em ordem (códigos crescentes)")
        print("12 - Exibir em pré-ordem (hierarquia da raiz)")
        print("13 - Exibir em pós-ordem (filhos antes do pai)")
        print("0 - Voltar")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            cadastrar_ordem()

        elif opcao == "2":
            consultar_ordem()

        elif opcao == "3":
            listar_ordens()

        elif opcao == "4":
            alterar_status()

        elif opcao == "5":
            alterar_prioridade()

        elif opcao == "6":
            registrar_servico()

        elif opcao == "7":
            remover_ordem()

        elif opcao == "8":
            processar_proxima_ordem()

        elif opcao == "9":
            relatorio_por_prioridade()

        elif opcao == "10":
            relatorio_por_valor()

        elif opcao == "11":
            exibir_em_ordem()

        elif opcao == "12":
            exibir_pre_ordem()

        elif opcao == "13":
            exibir_pos_ordem()

        elif opcao == "0":
            break

        else:
            print("Opção inválida.")

def main():
    while True:
        print("\n================================")
        print("          ERP OFICINA")
        print("================================")

        print("1 - Clientes e Veículos")
        print("2 - Estoque e Peças")
        print("3 - Ordens de Serviço")
        print("0 - Sair")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            menu_clientes_veiculos()

        elif opcao == "2":
            menu_estoque()

        elif opcao == "3":
            menu_ordens()

        elif opcao == "0":
            print("\nERP encerrado.")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
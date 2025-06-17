from datetime import datetime

saldo = 0
movimentos = []
saques_dia = {}


def exibir_menu():
    print("\nMenu:")
    print("1. Depositar")
    print("2. Sacar")
    print("3. Exibir Saldo")
    print("4. Exibir Movimentos")
    print("5. Sair")

    while True:
        try:
            opcao = int(input("Escolha uma opção: "))
            if opcao == 1:
                depositar()
            elif opcao == 2:
                sacar()
            elif opcao == 3:
                exibir_saldo()
            elif opcao == 4:
                exibir_movimentos()
            elif opcao == 5:
                print("Saindo do sistema. Até logo!")
                break
            else:
                print("Opção inválida. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Por favor, insira um número.")

def depositar():
    global saldo
    while True:
        try:
            valor = float(input("Digite o valor a ser depositado: "))
            if valor <= 0:
                print("O valor do depósito deve ser positivo.")
            else:
                saldo += valor
                data = datetime.now().strftime("%d%m/%Y %H:%M:%S")
                movimentos.append(f"Depósito: R$ {valor:.2f} - {data}")
                print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
                break
        except ValueError:
            print("Entrada inválida. Por favor, insira um número.")

def sacar():
    global saldo, saques_dia
    dataCompleta = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    data = datetime.now().strftime("%d/%m/%Y")
    if data not in saques_dia:
        saques_dia[data] = 0
    if saques_dia[data] >= 3:
        print("Limite de saques diários atingido. Você só pode sacar até 3 vezes por dia.")
        return
    while True:
        try:
            valor = float(input("Digite o valor a ser sacado: "))
            if valor <= 0:
                print("O valor do saque deve ser positivo.")
            elif valor > saldo:
                print("Saldo insuficiente para realizar o saque.")
                return
            elif valor > 500:
                print("O valor do saque não pode ser maior que R$ 500,00.")
            else:
                saldo -= valor
                movimentos.append(f"Saque: R$ {valor:.2f} - {dataCompleta}")
                saques_dia[data] += 1
                print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
                break
        except ValueError:
            print("Entrada inválida. Por favor, insira um número.")

def exibir_saldo():
    print(f"Saldo atual: R$ {saldo:.2f}")

def exibir_movimentos():
    if not movimentos:
        print("Nenhum movimento registrado.")
    else:
        print("Movimentos realizados:")
        for movimento in movimentos:
            print(movimento)
        print(f"\n saldo atual: R$ {saldo:.2f}")
# visualTemplate
print("Bem-vindo ao Sistema Bancário!")
exibir_menu()
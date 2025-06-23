from datetime import datetime

class Conta:
    
    contador = 1  # Corrigido: começa do número 1

    def __init__(self, cliente):
        self.cliente = cliente
        self.numero = Conta.contador
        Conta.contador += 1
        self.saldo = 0.0
        self.movimentos = []
        self.saques_dia = {} 

    def depositar(self):
        try:
            valor = float(input("Digite o valor a ser depositado: "))
            if valor <= 0:
                print("O valor do depósito deve ser positivo.")
            else:
                self.saldo += valor
                data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                self.movimentos.append(f"Depósito: R$ {valor:.2f} - {data}")
                print(f"Depósito de R$ {valor:.2f} realizado na conta {self.numero}.")
        except ValueError:
            print("Entrada inválida. Por favor, insira um número.")

    def sacar(self):
        data = datetime.now().strftime("%d/%m/%Y")
        if self.saques_dia.get(data, 0) >= 3:
            print("Limite de saques diários atingido. Você só pode sacar até 3 vezes por dia.")
            return
        try:
            valor = float(input("Digite o valor a ser sacado: "))
            if valor <= 0 or valor > self.saldo or valor > 500:
                print("Valor inválido. O valor do saque deve ser positivo, não pode exceder o saldo e não pode ser maior que R$ 500.")
            else:
                self.saldo -= valor
                self.saques_dia[data] = self.saques_dia.get(data, 0) + 1
                hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                self.movimentos.append(f"Saque: R$ {valor:.2f} - {hora}")
                print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
        except ValueError:
            print("Digite um valor válido para o saque.")

    def exibir_saldo(self):
        print(f"Saldo atual da conta {self.numero}: R$ {self.saldo:.2f}")

    def exibir_movimentos(self):
        if not self.movimentos:
            print("Nenhum movimento registrado.")
        else:
            print(f"Movimentos realizados da conta {self.numero}:")
            for movimento in self.movimentos:
                print(movimento)
            print(f"Saldo atual: R$ {self.saldo:.2f}")


class Cliente:
    def __init__(self, cpf, nome, nascimento, endereco):
        self.cpf = cpf
        self.nome = nome
        self.contas = []
        self.agencia = "0001"  # Atribuição fixa da agência
        self.nascimento = nascimento
        self.endereco = endereco

    def __str__(self):
        return f"Cliente: {self.nome}, CPF: {self.cpf}, contas: {len(self.contas)}"


def cadastrar_cliente(clientes):
    cpf = input("Digite o CPF do cliente (apenas números): ").strip()
    if cpf in clientes:
        print("Cliente já cadastrado.")
        return None
    nome = input("Digite o nome do cliente: ").strip()
    nascimento = input("Digite a data de nascimento do cliente (dd/mm/aaaa): ").strip()
    endereco = input("Digite o endereço do cliente: ").strip()
    cliente = Cliente(cpf, nome, nascimento, endereco)
    clientes[cpf] = cliente
    print("Cliente cadastrado com sucesso!")
    return cliente

def criar_conta(cliente):
    conta = Conta(cliente)
    cliente.contas.append(conta)
    print(f"Conta número {conta.numero} criada com sucesso para o cliente {cliente.nome}.")

def escolher_conta(cliente):
    if not cliente.contas:
        print("Nenhuma conta cadastrada. Por favor, crie uma conta primeiro.")
        return None
    print("Contas disponíveis:")
    for i, conta in enumerate(cliente.contas, start=1):
        print(f"{i}. Conta número {conta.numero} - Saldo: R$ {conta.saldo:.2f}")
    try:
        escolha = int(input("Escolha a conta pelo número: "))
        if 1 <= escolha <= len(cliente.contas):
            return cliente.contas[escolha - 1]
        else:
            print("Escolha fora do intervalo.")
    except ValueError:
        print("Entrada inválida.")
    return None

def menu(conta):
    while True:
        print("\nMenu da Conta:")
        print("1. Depositar")
        print("2. Sacar")
        print("3. Exibir Saldo")
        print("4. Exibir Movimentos")
        print("5. Trocar de Conta")
        print("6. Sair do Sistema")
        opcao = input("Escolha: ")
        if opcao == "1":
            conta.depositar()
        elif opcao == "2":
            conta.sacar()
        elif opcao == "3":
            conta.exibir_saldo()
        elif opcao == "4":
            conta.exibir_movimentos()
        elif opcao == "5":
            break
        elif opcao == "6":
            print("Encerrando o sistema. Até logo!")
            exit()
        else:
            print("Opção inválida.")

def iniciar_sistema_bancario():
    clientes = {}
    while True:
        print("\n=== Sistema Bancário ===")
        print("1. Cadastrar Cliente")
        print("2. Acessar Cliente")
        print("3. Sair")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            cliente = cadastrar_cliente(clientes)
            if cliente:
                criar_conta(cliente)
        elif opcao == "2":
            cpf = input("Digite o CPF do cliente: ").strip()
            cliente = clientes.get(cpf)
            if cliente:
                while True:
                    print(f"\nBem-vindo, {cliente.nome}")
                    print("1. Criar nova conta")
                    print("2. Escolher conta existente")
                    print("3. Voltar ao menu principal")
                    acao = input("Escolha: ")
                    if acao == "1":
                        criar_conta(cliente)
                    elif acao == "2":
                        conta = escolher_conta(cliente)
                        if conta:
                            menu(conta)
                    elif acao == "3":
                        break
                    else:
                        print("Opção inválida.")
            else:
                print("Cliente não encontrado.")
        elif opcao == "3":
            print("Sistema encerrado.")
            break
        else:
            print("Opção inválida.")

# Execução
if __name__ == "__main__":
    iniciar_sistema_bancario()

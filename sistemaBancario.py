from abc import ABC, abstractmethod
from datetime import datetime

# === Modelo ===

class Cliente:
    def __init__(self, cpf, nome, nascimento, endereco):
        self.cpf = cpf
        self.nome = nome
        self.nascimento = nascimento
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)


class Conta:
    _contador = 1

    def __init__(self, cliente):
        self._numero = Conta._contador
        Conta._contador += 1

        self._cliente = cliente
        self._saldo = 0.0
        self._agencia = "0001"
        self._historico = Historico()
        self._limite_saques = 3
        self._limite_valor_saque = 500.0

    @classmethod
    def nova_conta(cls, cliente):
        return cls(cliente)

    @property
    def numero(self):
        return self._numero

    @property
    def saldo(self):
        return self._saldo

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saques_do_dia = [
            t for t in self.historico.transacoes if t["tipo"] == "Saque"
            and t["data"].split()[0] == datetime.now().strftime("%d-%m-%Y")
        ]
        if len(saques_do_dia) >= self._limite_saques:
            print("Limite diário de saques atingido.")
            return False

        if valor <= 0 or valor > self._saldo or valor > self._limite_valor_saque:
            print("Valor inválido para saque.")
            return False

        self._saldo -= valor
        print(f"Saque de R$ {valor:.2f} realizado com sucesso.")
        return True

    def depositar(self, valor):
        if valor <= 0:
            print("Valor inválido para depósito.")
            return False

        self._saldo += valor
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso.")
        return True


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        })


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)


# === Interface ===

clientes = []
contas = []

def encontrar_cliente_por_cpf(cpf):
    for cliente in clientes:
        if cliente.cpf == cpf:
            return cliente
    return None

def cadastrar_cliente():
    cpf = input("Digite o CPF do cliente (somente números): ").strip()
    if encontrar_cliente_por_cpf(cpf):
        print("Cliente já cadastrado.")
        return

    nome = input("Digite o nome do cliente: ").strip()
    nascimento = input("Digite a data de nascimento (dd/mm/aaaa): ").strip()
    endereco = input("Digite o endereço do cliente: ").strip()

    cliente = Cliente(cpf, nome, nascimento, endereco)
    clientes.append(cliente)
    print("Cliente cadastrado com sucesso!")

def criar_conta():
    cpf = input("Informe o CPF do cliente: ").strip()
    cliente = encontrar_cliente_por_cpf(cpf)
    if not cliente:
        print("Cliente não encontrado.")
        return

    conta = Conta.nova_conta(cliente)
    cliente.adicionar_conta(conta)
    contas.append(conta)
    print(f"Conta número {conta.numero} criada com sucesso!")

def selecionar_conta(cliente):
    if not cliente.contas:
        print("Este cliente não possui contas.")
        return None

    print("Contas disponíveis:")
    for i, conta in enumerate(cliente.contas):
        print(f"{i + 1}. Conta {conta.numero} (Saldo: R$ {conta.saldo:.2f})")

    try:
        opcao = int(input("Escolha o número da conta: "))
        return cliente.contas[opcao - 1] if 0 < opcao <= len(cliente.contas) else None
    except ValueError:
        return None

def depositar():
    cpf = input("CPF do cliente: ").strip()
    cliente = encontrar_cliente_por_cpf(cpf)
    if not cliente:
        print("Cliente não encontrado.")
        return

    conta = selecionar_conta(cliente)
    if not conta:
        print("Conta inválida.")
        return

    try:
        valor = float(input("Valor do depósito: "))
        transacao = Deposito(valor)
        cliente.realizar_transacao(conta, transacao)
    except ValueError:
        print("Valor inválido.")

def sacar():
    cpf = input("CPF do cliente: ").strip()
    cliente = encontrar_cliente_por_cpf(cpf)
    if not cliente:
        print("Cliente não encontrado.")
        return

    conta = selecionar_conta(cliente)
    if not conta:
        print("Conta inválida.")
        return

    try:
        valor = float(input("Valor do saque: "))
        transacao = Saque(valor)
        cliente.realizar_transacao(conta, transacao)
    except ValueError:
        print("Valor inválido.")

def exibir_extrato():
    cpf = input("CPF do cliente: ").strip()
    cliente = encontrar_cliente_por_cpf(cpf)
    if not cliente:
        print("Cliente não encontrado.")
        return

    conta = selecionar_conta(cliente)
    if not conta:
        print("Conta inválida.")
        return

    print("\n===== EXTRATO =====")
    if not conta.historico.transacoes:
        print("Nenhuma transação realizada.")
    else:
        for t in conta.historico.transacoes:
            print(f"{t['tipo']} - R$ {t['valor']:.2f} - {t['data']}")
    print(f"Saldo atual: R$ {conta.saldo:.2f}")
    print("===================")

def menu():
    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("[1] Cadastrar cliente")
        print("[2] Criar conta")
        print("[3] Depositar")
        print("[4] Sacar")
        print("[5] Exibir extrato")
        print("[6] Sair")

        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            cadastrar_cliente()
        elif opcao == "2":
            criar_conta()
        elif opcao == "3":
            depositar()
        elif opcao == "4":
            sacar()
        elif opcao == "5":
            exibir_extrato()
        elif opcao == "6":
            print("Encerrando sistema.")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()

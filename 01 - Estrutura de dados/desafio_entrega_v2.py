import textwrap
from typing import List
from abc import ABC, abstractmethod

# ----------------------------------------------------------------------
# classes


class Conta:
    AGENCIA = "0001"

    def __init__(self, numero_conta, cliente):
        self._saldo = 0
        self._numero_conta = numero_conta
        self._agencia = self.AGENCIA
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero_conta(self):
        return self._numero_conta

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    @classmethod
    def nova_conta(cls, cliente, numero_conta: int):
        return cls(numero_conta, cliente)

    def sacar(self, valor: float):
        excedeu_saldo = valor > self.saldo
        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
            return False

        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True

        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

    def depositar(self, valor: float):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
            return True

        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
        return False


class ContaCorrente(Conta):
    def __init__(self, numero_conta: str, cliente, limite=500, limite_saques=3):
        super().__init__(numero_conta, cliente)
        self._limite = limite
        self._limite_saques = limite_saques
        self._numero_saques = 0

    @property
    def limite(self):
        return self._limite

    @property
    def limite_saques(self):
        return self._limite_saques

    @property
    def numero_saques(self):
        return self._numero_saques

    def sacar(self, valor: float):
        excedeu_saldo = valor > self.saldo
        excedeu_limite = valor > self.limite
        excedeu_saques = len(self.historico.transacoes) >= self.limite_saques

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
            return False

        elif excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
            return False

        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
            return False

        elif valor > 0:
            self._saldo -= valor
            self._numero_saques += 1
            # extrato += f"Saque:\t\tR$ {valor:.2f}\n"
            print("\n=== Saque realizado com sucesso! ===")
            return True

        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta: Conta):
        pass


class Deposito(Transacao):
    def __init__(self, valor: float):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta: Conta):
        sucesso = conta.depositar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)


class Saque(Transacao):
    def __init__(self, valor: float):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso = conta.sacar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)


class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._lista_contas = []

    @property
    def lista_contas(self):
        return self._lista_contas

    @property
    def endereco(self):
        return self._endereco

    def realizar_transacao(self, transacao: Transacao, conta: Conta):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.lista_contas.append(conta)

    def selecionar_conta(self, numero_conta: int):
        contas_filtradas = [
            conta for conta in self.lista_contas if conta.numero_conta == numero_conta
        ]
        return contas_filtradas[0] if contas_filtradas else None


class PessoaFisica(Cliente):
    def __init__(self, cpf: str, nome: str, data_nascimento: str, endereco: str):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao: Transacao):
        self._transacoes.append(transacao)


# ------------------------------------------------------------------------------


def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))


def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    pass
    # excedeu_saldo = valor > saldo
    # excedeu_limite = valor > limite
    # excedeu_saques = numero_saques >= limite_saques

    # if excedeu_saldo:
    #     print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

    # elif excedeu_limite:
    #     print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

    # elif excedeu_saques:
    #     print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

    # elif valor > 0:
    #     saldo -= valor
    #     extrato += f"Saque:\t\tR$ {valor:.2f}\n"
    #     numero_saques += 1
    #     print("\n=== Saque realizado com sucesso! ===")

    # else:
    #     print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    # return saldo, extrato


def exibir_extrato(saldo, /, *, extrato):
    pass
    # print("\n================ EXTRATO ================")
    # print("Não foram realizadas movimentações." if not extrato else extrato)
    # print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    # print("==========================================")


def criar_usuario(lista_usuarios, cpf=None):
    if not cpf:
        cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, lista_usuarios)

    if usuario:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return None

    print("Vamos precisar de algumas informações:")
    nome = input("Nome completo: ")
    data_nascimento = input("Data de nascimento (dd-mm-aaaa): ")
    endereco = input(
        "Endereço (logradouro, nro - bairro - cidade/sigla estado - cep): "
    )
    usuario = PessoaFisica(
        nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco
    )

    lista_usuarios.append(usuario)

    print("=== Usuário criado com sucesso! ===")
    return usuario


def filtrar_usuario(cpf, lista_usuarios):
    usuarios_filtrados = [
        usuario for usuario in lista_usuarios if usuario["cpf"] == cpf
    ]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def recuperar_usuario(lista_usuarios, cpf):
    usuario = filtrar_usuario(cpf, lista_usuarios)
    if not usuario:
        opcao = input(
            "Usuário não cadastrado. Gostaria de criar um novo usuário? (s/n):"
        )
        if opcao.lower() == "s":
            usuario = criar_usuario(lista_usuarios, cpf)
        else:
            print("Operação encerrada.")
            return None

    return usuario


def criar_conta(agencia, numero_conta, usuarios):
    pass
    # cpf = input("Informe o CPF do usuário: ")
    # usuario = filtrar_usuario(cpf, usuarios)

    # if usuario:
    #     print("\n=== Conta criada com sucesso! ===")
    #     return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    # print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")


def listar_contas(lista_contas: List[Conta]):
    # pass
    for conta in lista_contas:
        linha = f"""\
            Agência:\t{conta.agencia}
            Número da Conta (C/C):\t\t{conta.numero_conta}
            Titular:\t{conta.cliente.nome}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))


def recuperar_conta_usuario(usuario: Cliente):
    conta = None
    if not usuario.lista_contas:
        print("Usuário ainda não possui conta. Vamos criar uma nova conta para ele.")
        numero_conta = len(usuario.lista_contas) + 1
        nova_conta = ContaCorrente.nova_conta(usuario, numero_conta)
        usuario.adicionar_conta(nova_conta)
        conta = nova_conta
    elif len(usuario.lista_contas) == 1:
        return usuario.lista_contas[0]
    else:
        listar_contas(usuario.lista_contas)
        numero_conta = int(input("Informe o número da conta: "))
        conta = usuario.selecionar_conta(numero_conta)

        if not conta:
            print("\n@@@ Conta não encontrada para o usuário informado! @@@")

    return conta


# ----------------------------------------------------------------------------
def main():
    # LIMITE_SAQUES = 3
    # AGENCIA = "0001"

    # saldo = 0
    # limite = 500
    # extrato = ""
    # numero_saques = 0
    lista_usuarios = []
    lista_contas = []

    cpf = input("Olá, bem vindo ao DIO Bank! Por favor, informe o seu CPF:")
    usuario = recuperar_usuario(lista_usuarios, cpf)
    if usuario is None:
        print("Usuário não encontrado. Operação finalizada.")
        exit()

    conta_ativa = recuperar_conta_usuario(usuario)
    print(f"Olá {usuario.nome}, seja bem vindo!")

    while True:
        opcao = menu()

        if opcao == "d":
            pass
            # valor = float(input("Informe o valor do depósito: "))

            # saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            pass
            # valor = float(input("Informe o valor do saque: "))

            # saldo, extrato = sacar(
            #     saldo=saldo,
            #     valor=valor,
            #     extrato=extrato,
            #     limite=limite,
            #     numero_saques=numero_saques,
            #     limite_saques=LIMITE_SAQUES,
            # )

        elif opcao == "e":
            pass
            # exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            pass
            # criar_usuario(lista_usuarios)

        elif opcao == "nc":
            pass
            # numero_conta = len(lista_contas) + 1
            # conta = criar_conta(AGENCIA, numero_conta, lista_usuarios)

            # if conta:
            #     lista_contas.append(conta)

        elif opcao == "lc":
            pass
            # listar_contas(lista_contas)

        elif opcao == "q":
            break

        else:
            print(
                "Operação inválida, por favor selecione novamente a operação desejada."
            )


main()

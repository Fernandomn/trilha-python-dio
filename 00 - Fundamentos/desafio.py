agencia = "0001"
lista_usuarios = []
LIMITE_SAQUES = 3
menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[u] Mudar Usuário
[q] Sair

=> """


class Usuario:

    def __init__(self, nome, data_nascimento, cpf, endereco):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.endereco = endereco
        self.lista_contas = []

    def criar_conta(self, agencia, numero_conta):
        nova_conta = Conta(agencia, numero_conta, self.cpf)
        self.lista_contas.append(nova_conta)
        return nova_conta

    def recuperar_conta_por_numero(self, numero_conta):
        return next(
            (
                conta
                for conta in self.lista_contas
                if conta.numero_conta == numero_conta
            ),
            None,
        )

    def recuperar_conta_usuario(self):
        if len(self.lista_contas) == 0:
            global agencia
            print("Usuário não possui conta. Vamos criar uma nova conta para ele.")
            numero_conta = len(self.lista_contas) + 1
            nova_conta = self.criar_conta(agencia, numero_conta)
            return (self, nova_conta)
        elif len(self.lista_contas) == 1:
            return (self, self.lista_contas[0])
        else:
            print("O usuário possui mais de uma conta. Selecione qual deseja acessar:")
            for conta in self.lista_contas:
                print(f"Conta número: {conta.numero_conta} - Agência: {conta.agencia}")
            numero_conta = int(input("Informe o número da conta que deseja acessar: "))
            conta_selecionada = self.recuperar_conta_por_numero(numero_conta)
            if conta_selecionada is None:
                print("Número de conta inválido. Operação encerrada.")
                return None
            return conta_selecionada


class Conta:
    def __init__(self, agencia, numero_conta, cpf_usuario):
        self.agencia = agencia
        self.numero_conta = numero_conta
        self.cpf_usuario = cpf_usuario
        self.saldo = 0
        self.limite = 500
        self.numero_saques = 0
        self.lista_extrato = []


def sacar(*, valor, saldo, limite, numero_saques, limite_saques=LIMITE_SAQUES, extrato):
    excedeu_saldo = valor > saldo

    excedeu_limite = valor > limite

    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")

    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")

    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")

    elif valor > 0:
        atualizar_saldo(-valor)
        atualizar_extrato(extrato, "Saque", valor)
        atualizar_numero_saques()

    else:
        print("Operação falhou! O valor informado é inválido.")


def depositar(valor, extrato, /):
    if valor > 0:
        atualizar_saldo(valor)
        atualizar_extrato(extrato, "Deposito", valor)

    else:
        print("Operação falhou! O valor informado é inválido.")


def visualizar_historico(saldo, extrato):
    pass


def criar_usuario(nome, data_nascimento, cpf, endereco):
    novo_usuario = None
    if any(usuario.cpf == cpf for usuario in lista_usuarios):
        print("Já existe um usuário cadastrado com esse CPF.")
    else:
        novo_usuario = Usuario(nome, data_nascimento, cpf, endereco)
        lista_usuarios.append(novo_usuario)
    return novo_usuario


def recuperar_usuario(cpf):
    possiveis_usuarios = [usuario.cpf == cpf for usuario in lista_usuarios]
    usuario = None
    if not len(possiveis_usuarios):
        opcao = input(
            "Usuário não cadastrado. Gostaria de criar um novo usuário? (s/n):"
        )
        if opcao.lower() == "s":
            print("Vamos pedir algumas informações:")
            nome = input("Nome completo: ")
            data_nascimento = input("Data de nascimento (dd-mm-aaaa): ")
            endereco = input(
                "Endereço (logradouro, nro - bairro - cidade/sigla estado - cep): "
            )
            usuario = criar_usuario(nome, data_nascimento, cpf, endereco)
        else:
            print("Operação encerrada.")
            return None
    else:
        usuario = possiveis_usuarios[0]

    return (usuario, usuario.recuperar_conta_usuario())


def atualizar_extrato(extrato, tipo_operacao, valor):
    extrato.append(f"{tipo_operacao}: R$ {valor:.2f}\n")


def imprimir_extrato(extrato, saldo):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else "".join(extrato))
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")


def atualizar_saldo(valor):
    global saldo
    saldo += valor


def atualizar_numero_saques():
    global numero_saques
    numero_saques += 1


# ----------------------------------------------------------------------

cpf = input("Olá, bem vindo ao DIO Bank! Por favor, informe o seu CPF:")
usuario, conta_ativa = recuperar_usuario(cpf)

if usuario == None:
    print("Usuário não encontrado. Operação finalizada.")
    exit()
print(f"Olá {usuario.nome}, seja bem vindo!")

while True:

    opcao = input(menu)

    if opcao == "d":
        valor = float(input("Informe o valor do depósito: "))
        depositar(valor, conta_ativa.lista_extrato)

    elif opcao == "s":
        valor = float(input("Informe o valor do saque: "))
        sacar(
            valor=valor,
            saldo=saldo,
            limite=conta_ativa.limite,
            numero_saques=numero_saques,
            extrato=conta_ativa.lista_extrato,
        )

    elif opcao == "e":
        imprimir_extrato(conta_ativa.lista_extrato, saldo)

    elif opcao == "u":
        cpf = input("Por favor, informe o CPF do usuário:")
        (novo_usuario, nova_conta) = recuperar_usuario(cpf)
        if novo_usuario == None:
            print(f"Usuário não encontrado. Vamos continuar com {usuario.nome}, ok?")
        else:
            usuario = novo_usuario
            conta_ativa = nova_conta
            print(f"Olá {usuario.nome}, seja bem vindo!")

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")

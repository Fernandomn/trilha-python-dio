agencia = "0001"
menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[u] Mudar Usuário
[q] Sair

=> """
usuario = None
saldo = 0
limite = 500
numero_saques = 0
lista_extrato = []
lista_usuarios = []
LIMITE_SAQUES = 3


class Usuario:
    lista_contas = []

    def __init__(self, nome, data_nascimento, cpf, endereco):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.endereco = endereco


class Conta:
    def __init__(self, numero_conta, usuario):
        global agencia
        self.agencia = agencia
        self.numero_conta = numero_conta
        self.usuario = usuario


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
    else:
        usuario = possiveis_usuarios[0]
    lista_usuarios
    return usuario


def criar_conta(agencia, numero_conta, usuario):
    pass


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

usuario = recuperar_usuario(cpf)
if usuario == None:
    print("Usuário não encontrado. Operação finalizada.")
    exit()
print(f"Olá {usuario.nome}, seja bem vindo!")

while True:

    opcao = input(menu)

    if opcao == "d":
        valor = float(input("Informe o valor do depósito: "))
        depositar(valor, lista_extrato)

    elif opcao == "s":
        valor = float(input("Informe o valor do saque: "))
        sacar(
            valor=valor,
            saldo=saldo,
            limite=limite,
            numero_saques=numero_saques,
            extrato=lista_extrato,
        )

    elif opcao == "e":
        imprimir_extrato(lista_extrato, saldo)

    elif opcao == "u":
        cpf = input("Por favor, informe o CPF do usuário:")
        novo_usuario = recuperar_usuario(cpf)
        if novo_usuario == None:
            print(f"Usuário não encontrado. Vamos continuar com {usuario.nome}, ok?")
        else:
            usuario = novo_usuario
            print(f"Olá {usuario.nome}, seja bem vindo!")

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")

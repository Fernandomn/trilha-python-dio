agencia = "0001"
lista_usuarios = []
LIMITE_SAQUES = 3
menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[u] Mudar Usuário
[c] Mudar Conta
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

    def exibir_contas(self):
        print("\n".join(self.lista_contas))

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
            return nova_conta
        elif len(self.lista_contas) == 1:
            return self.lista_contas[0]
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

    def atualizar_extrato(self, tipo_operacao, valor):
        self.lista_extrato.append(f"{tipo_operacao}: R$ {valor:.2f}\n")

    def imprimir_extrato(self):
        print("\n================ EXTRATO ================")
        print(
            "Não foram realizadas movimentações."
            if not self.lista_extrato
            else "".join(self.lista_extrato)
        )
        print(f"\nSaldo: R$ {self.saldo:.2f}")
        print("==========================================")

    def atualizar_saldo(self, valor):
        self.saldo += valor

    def atualizar_numero_saques(self):
        numero_saques += 1

    def sacar(self, *, valor, limite_saques=LIMITE_SAQUES):
        excedeu_saldo = valor > self.saldo

        excedeu_limite = valor > self.limite

        excedeu_saques = self.numero_saques >= limite_saques

        if excedeu_saldo:
            print("Operação falhou! Você não tem saldo suficiente.")

        elif excedeu_limite:
            print("Operação falhou! O valor do saque excede o limite.")

        elif excedeu_saques:
            print("Operação falhou! Número máximo de saques excedido.")

        elif valor > 0:
            self.atualizar_saldo(-valor)
            self.atualizar_extrato("Saque", valor)
            self.atualizar_numero_saques()

        else:
            print("Operação falhou! O valor informado é inválido.")

    def depositar(self, valor, /):
        if valor > 0:
            self.atualizar_saldo(valor)
            self.atualizar_extrato("Deposito", valor)

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
    possiveis_usuarios = [usuario for usuario in lista_usuarios if usuario.cpf == cpf]
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

    return usuario


# ----------------------------------------------------------------------

cpf = input("Olá, bem vindo ao DIO Bank! Por favor, informe o seu CPF:")
usuario = recuperar_usuario(cpf)
conta_ativa = usuario.recuperar_conta_usuario()

if usuario == None:
    print("Usuário não encontrado. Operação finalizada.")
    exit()
print(f"Olá {usuario.nome}, seja bem vindo!")

while True:

    opcao = input(menu)

    if opcao == "d":
        valor = float(input("Informe o valor do depósito: "))
        conta_ativa.depositar(valor)

    elif opcao == "s":
        valor = float(input("Informe o valor do saque: "))
        conta_ativa.sacar(
            valor=valor,
        )

    elif opcao == "e":
        conta_ativa.imprimir_extrato()

    elif opcao == "u":
        cpf = input("Por favor, informe o CPF do usuário:")
        novo_usuario = recuperar_usuario(cpf)
        if novo_usuario == None:
            print(f"Usuário não encontrado. Vamos continuar com {usuario.nome}, ok?")
        else:
            usuario = novo_usuario
            print(f"Olá {usuario.nome}, seja bem vindo!")
            conta_ativa = novo_usuario.recuperar_conta_usuario()
    elif opcao == "c":
        if len(usuario.lista_contas) == 0:
            exit()
        elif len(usuario.lista_contas) == 1:
            criar_nova_conta = input(
                "Usuário possui apenas uma conta. Deseja criar uma nova conta? (s/n)"
            )
            if criar_nova_conta.lower() == "s":
                numero_conta = len(usuario.lista_contas) + 1
                nova_conta = usuario.criar_conta(agencia, numero_conta)
                conta_ativa = nova_conta
                print(
                    f"Nova conta número {conta_ativa.numero_conta} criada e selecionada com sucesso!"
                )
        else:
            print("O usuário possui mais de uma conta. Selecione qual deseja acessar:")
            usuario.exibir_contas()
            numero_conta = int(input("Informe o número da conta que deseja acessar: "))
            conta_selecionada = usuario.recuperar_conta_por_numero(numero_conta)
            if conta_selecionada is None:
                print(
                    "Número de conta inválido. Vamos continuar com a conta atual, ok?"
                )
            else:
                conta_ativa = conta_selecionada
                print(
                    f"Conta número {conta_ativa.numero_conta} selecionada com sucesso!"
                )

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")

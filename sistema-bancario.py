import textwrap


def menu():
    menu = """\n
    *****MENU*****
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo Usuário
    [q]\tSair
    -->
    """
    return input(textwrap.dedent(menu))


def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Deposito de {valor} \n"
        print("\nDeposito feito com sucesso")
    else:
        print("Valor inválido")

    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_saques = numero_saques > limite_saques
    excedeu_limite = valor > limite

    if excedeu_saldo:
        print("\n Saldo insuficiente")

    elif excedeu_limite:
        print("\n Limite permitido excedido, tente um valor mais baixo")

    elif excedeu_saques:
        print("\n Limite de saques diarios excedidos, tente novamente amanhã")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque de R${valor} \n"
        numero_saques += 1
        print("Saque realizado com sucesso")

    else:
        print("@@@Operação inválida, tente novamente!")

    return saldo, extrato


def exibir_extrato(saldo, /, *, extrato):
    saldo_total = f"Saldo total R${saldo}\n"
    extrato += saldo_total
    return print(extrato)


def criar_usuario(usuarios):
    cpf = input("Digite seu cpf (somente numero): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("Usuário já cadastrado")
        return

    nome = input("Digite seu nome completo: ")
    data_nascimento = input("Digite sua data de nascimento (dd-mm-aaaa): ")
    endereco = input(
        "Digite seu endereço (logradouro - n° - bairro - cidade/sigla estado): "
    )
    usuarios.append(
        {
            "nome": nome,
            "cpf": cpf,
            "data_nascimento": data_nascimento,
            "endereco": endereco,
        }
    )
    print("Usuário criado com sucesso")


def filtrar_usuario(cpf, usuarios):
    usuario_filtrado = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuario_filtrado[0] if usuario_filtrado else None


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Digite seu cpf (apenas numeros): ")
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print("Conta criada com sucesso")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\n@@@Usuário não encontrado!@@@")
    return None


def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t {conta["agencia"]}
            Conta:\t {conta['numero_conta']}
            Titular:\t {conta['usuario']['nome']}
            """
        print("*" * 100)
        print(textwrap.dedent(linha))


def main():
    agencia = "0001"
    LIMITE_SAQUES = 3
    limite = 500
    saldo = 0
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []
    nro_conta = 1

    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o valor que quer depositar: "))

            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))

            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nc":
            numero_de_conta = nro_conta
            nova_conta = criar_conta(agencia, numero_de_conta, usuarios)
            if nova_conta:
                contas.append(nova_conta)
                nro_conta += 1

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "q":
            break

        else:
            print("Operação inválida!")


main()

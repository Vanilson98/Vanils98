import textwrap

class Usuario:
    def __init__(self, nome, data_nascimento, cpf, endereco):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.endereco = endereco

class ContaBancaria:
    LIMITE_SAQUES = 3

    def __init__(self, agencia, numero_conta, usuario):
        self.agencia = agencia
        self.numero_conta = numero_conta
        self.usuario = usuario
        self.saldo = 0.0
        self.extrato = ""
        self.limite = 500.0
        self.numero_saques = 0

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.extrato += f"Depósito:\tR$ {valor:.2f}\n"
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    def sacar(self, valor):
        excedeu_saldo = valor > self.saldo
        excedeu_limite = valor > self.limite
        excedeu_saques = self.numero_saques >= ContaBancaria.LIMITE_SAQUES

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
        elif excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
        elif valor > 0:
            self.saldo -= valor
            self.extrato += f"Saque:\t\tR$ {valor:.2f}\n"
            self.numero_saques += 1
            print("\n=== Saque realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    def exibir_extrato(self):
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not self.extrato else self.extrato)
        print(f"\nSaldo:\t\tR$ {self.saldo:.2f}")
        print("==========================================")

class Banco:
    def __init__(self):
        self.usuarios = []
        self.contas = []

    def criar_usuario(self, nome, data_nascimento, cpf, endereco):
        if self.filtrar_usuario(cpf):
            print("\n@@@ Já existe usuário com esse CPF! @@@")
        else:
            usuario = Usuario(nome, data_nascimento, cpf, endereco)
            self.usuarios.append(usuario)
            print("=== Usuário criado com sucesso! ===")

    def criar_conta(self, agencia, usuario_cpf):
        usuario = self.filtrar_usuario(usuario_cpf)
        if usuario:
            numero_conta = len(self.contas) + 1
            conta = ContaBancaria(agencia, numero_conta, usuario)
            self.contas.append(conta)
            print("\n=== Conta criada com sucesso! ===")
        else:
            print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")

    def listar_contas(self):
        for conta in self.contas:
            linha = f"""\
                Agência:\t{conta.agencia}
                C/C:\t\t{conta.numero_conta}
                Titular:\t{conta.usuario.nome}
            """
            print("=" * 100)
            print(textwrap.dedent(linha))

    def filtrar_usuario(self, cpf):
        for usuario in self.usuarios:
            if usuario.cpf == cpf:
                return usuario
        return None

def menu():
    menu_texto = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu_texto))

def main():
    banco = Banco()
    AGENCIA = "0001"

    while True:
        opcao = menu()

        if opcao == "d":
            cpf = input("Informe o CPF do usuário: ")
            usuario = banco.filtrar_usuario(cpf)
            if usuario:
                conta = next((conta for conta in banco.contas if conta.usuario.cpf == cpf), None)
                if conta:
                    valor = float(input("Informe o valor do depósito: "))
                    conta.depositar(valor)
                else:
                    print("\n@@@ Conta não encontrada! @@@")
            else:
                print("\n@@@ Usuário não encontrado! @@@")

        elif opcao == "s":
            cpf = input("Informe o CPF do usuário: ")
            usuario = banco.filtrar_usuario(cpf)
            if usuario:
                conta = next((conta for conta in banco.contas if conta.usuario.cpf == cpf), None)
                if conta:
                    valor = float(input("Informe o valor do saque: "))
                    conta.sacar(valor)
                else:
                    print("\n@@@ Conta não encontrada! @@@")
            else:
                print("\n@@@ Usuário não encontrado! @@@")

        elif opcao == "e":
            cpf = input("Informe o CPF do usuário: ")
            usuario = banco.filtrar_usuario(cpf)
            if usuario:
                conta = next((conta for conta in banco.contas if conta.usuario.cpf == cpf), None)
                if conta:
                    conta.exibir_extrato()
                else:
                    print("\n@@@ Conta não encontrada! @@@")
            else:
                print("\n@@@ Usuário não encontrado! @@@")

        elif opcao == "nu":
            nome = input("Informe o nome completo: ")
            data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
            cpf = input("Informe o CPF (somente números): ")
            endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
            banco.criar_usuario(nome, data_nascimento, cpf, endereco)

        elif opcao == "nc":
            cpf = input("Informe o CPF do usuário: ")
            banco.criar_conta(AGENCIA, cpf)

        elif opcao == "lc":
            banco.listar_contas()

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

if __name__ == "__main__":
    main()

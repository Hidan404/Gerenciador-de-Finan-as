from model.models import *
from views.view import *


class Ui():
    def __init__(self):
        self.contas = listar_contas()

    def menu(self):
        print("1 - Criar conta")
        print("2 - Listar contas")
        print("3 - Desativar conta")
        print("4 - Remover conta")
        print("5 - Criar grafico")
        print("6 - Sair")
        opcao = int(input("Digite a opção: "))

        if opcao == 1:
            self.criar_conta()
        elif opcao == 2:
            self.listar_contas()
        elif opcao == 3:
            self.desativar_conta()
        elif opcao == 4:
            self.remover_conta()
        elif opcao == 5:
            self.criar_grafico()    
        elif opcao == 6:
            exit()

    def criar_conta(self):
        nome = input("Digite o nome da conta: ")
        saldo = float(input("Digite o saldo da conta: "))
        banco = int(input("Digite o id do banco: "))
        tipo = int(input("Digite o id do tipo: "))
        conta = Conta(nome=nome, saldo=saldo, banco_id=banco, tipo_id=tipo)
        conta = criar_conta(conta)
        self.contas.append(conta)

    def listar_contas(self):
        for conta in self.contas:
            print(f"Nome: {conta.nome}, Saldo: {conta.saldo}, Banco: {conta.banco.nome}, Tipo: {conta.tipo.nome}")

    def desativar_conta(self):
        id = int(input("Digite o id da conta: "))
        conta = desativar_conta(id)
        if conta:
            print(f"Conta {conta.nome} desativada")
    def criar_grafico(self):
        contas = listar_contas()
        nomes = [conta.nome for conta in contas]
        saldos = [conta.saldo for conta in contas]

        plt.bar(nomes, saldos)
        plt.show()
    def remover_conta(self):
        id = int(input("Digite o id da conta: "))
        conta = remover_conta(id)
        if conta:
            print(f"Conta {conta.nome} removida")


Ui().menu()            
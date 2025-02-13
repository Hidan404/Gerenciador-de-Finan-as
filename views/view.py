from model.models import Conta, engine, Bancos, StatusConta
from sqlalchemy.orm import Session
from sqlalchemy import select


def criar_conta(conta: Conta):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.nome == conta.nome)
        results = session.execute(statement).scalars().all()

        if results:
            print("Conta já existe")
            return
        else:
            print("Conta criada")
        session.add(conta)
        session.commit()

        return conta

def listar_contas():
    with Session(engine) as session:
        statement = select(Conta)
        results = session.execute(statement)
        contas = results.scalars().all()

        return contas
    
def desativar_conta(id):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.id == id)
        results = session.execute(statement).scalars().all()

        if not results:
            print("Conta não encontrada")
            return

        conta = results[0]
        if conta.saldo >= 0:
            print("Conta com saldo positivo nao pode ser desativada")
            return
        conta.status = StatusConta.INATIVA
        session.add(conta)
        session.commit()

        return conta    

def remover_conta(id):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.id == id)
        results = session.execute(statement).scalars().all()

        if not results:
            print("Conta não encontrada")
            return

        conta = results[0]
        session.delete(conta)
        session.commit()

        return conta
    

def transferir_saldo(conta_origem_id, conta_destino_id, valor):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.id == conta_origem_id)
        results = session.execute(statement).scalars().all()

        if not results:
            print("Conta de origem não encontrada")
            return

        conta_origem = results[0]
        if conta_origem.saldo < valor:
            print("Saldo insuficiente")
            return

        statement = select(Conta).where(Conta.id == conta_destino_id)
        results = session.execute(statement).scalars().all()

        if not results:
            print("Conta de destino não encontrada")
            return

        conta_destino = results[0]
        conta_origem.saldo -= valor
        conta_destino.saldo += valor
        session.add(conta_origem)
        session.add(conta_destino)
        session.commit()

        return conta_origem, conta_destino   

conta = Conta(nome = "Sabrina", banco = Bancos.SANTANDER, tipo = "Conta Corrente", saldo = 3000.0, usuario_id = 2, status = StatusConta.ATIVA) 
conta2 = Conta(nome = "hidan", banco = Bancos.INTER, tipo = "Conta Corrente", saldo = 3000.0, usuario_id = 2, status = StatusConta.ATIVA) 
conta3 = Conta(nome = "konan", banco = Bancos.INTER, tipo = "Conta Corrente", saldo = 3000.0, usuario_id = 3, status = StatusConta.ATIVA)
criar_conta(conta3)
print(listar_contas())
print(desativar_conta(2))
print(transferir_saldo(2, 3, 1000))


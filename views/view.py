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

conta = Conta(nome = "Sabrina", banco = Bancos.SANTANDER, tipo = "Conta Corrente", saldo = 3000.0, usuario_id = 2, status = StatusConta.ATIVA)  

criar_conta(conta)
print(listar_contas())
print(desativar_conta(2))


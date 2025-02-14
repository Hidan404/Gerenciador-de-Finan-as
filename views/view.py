from model.models import Conta, engine, Bancos, StatusConta, Historico, Tipos
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import date, timedelta

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

        taxa = 0.01
        valor -= valor * taxa

        conta_destino = results[0]
        conta_origem.saldo -= valor
        conta_destino.saldo += valor
        session.add(conta_origem)
        session.add(conta_destino)
        session.commit()

        return conta_origem, conta_destino   
    
def movimentar_dinheiro(historico: Historico):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.id == historico.conta_id)
        results = session.execute(statement).scalars().all()
        #TODO: validar se a conta esta ativa
        if not results:
            print("Conta não encontrada")
            return

        conta = results[0]
        if historico.tipo == Tipos.SAIDA and conta.saldo < historico.valor:
            print("Saldo insuficiente")
            return
        
        if historico.tipo == Tipos.ENTRADA:
            conta.saldo += historico.valor
        else:
            conta.saldo -= historico.valor    

        conta.saldo += historico.valor
        session.add(conta)
        session.commit()
        print("Movimentação realizada com sucesso")


def total_contas():
    with Session(engine) as session:
        statement = select(Conta)
        results = session.execute(statement)
        contas = results.scalars().all()

        total = 0
        for conta in contas:
            total += conta.saldo

        return total    

def buscar_historico_entre_datas(data_inicial, data_final):
    with Session(engine) as session:
        statement = select(Historico).where(Historico.data >= data_inicial).where(Historico.data <= data_final)
        results = session.execute(statement)
        historicos = results.scalars().all()

        return historicos        

conta = Conta(nome = "Sabrina", banco = Bancos.SANTANDER, tipo = "Conta Corrente", saldo = 3000.0, usuario_id = 2, status = StatusConta.ATIVA) 
conta2 = Conta(nome = "hidan", banco = Bancos.INTER, tipo = "Conta Corrente", saldo = 3000.0, usuario_id = 2, status = StatusConta.ATIVA) 
conta3 = Conta(nome = "konan", banco = Bancos.INTER, tipo = "Conta Corrente", saldo = 3000.0, usuario_id = 3, status = StatusConta.ATIVA)
criar_conta(conta3)


historico = Historico(conta_id = 3, tipo = Tipos.ENTRADA, valor = 100.0, data = date.today())

movimentar_dinheiro(historico)

with Session(engine) as session:
    statement = select(Historico)
    results = session.execute(statement).scalars().all()

    for h in results:
        print(h)

print(total_contas())
print(buscar_historico_entre_datas(date.today() - timedelta(days=1), date.today() + timedelta(days=1)))
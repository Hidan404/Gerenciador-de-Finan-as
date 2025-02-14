import sqlmodel
from sqlmodel import Relationship
import enum
from datetime import date

class Bancos(enum.Enum):
    NUBANK = "Nubank"
    SANTANDER = "Santander"
    INTER = "Inter"

class StatusConta(enum.Enum):
    ATIVA = "Ativa"
    INATIVA = "Inativa"

class Tipos(enum.Enum):
    ENTRADA = "Entrada"
    SAIDA = "Saida"    

class Conta(sqlmodel.SQLModel, table=True):
    id: int = sqlmodel.Field(default=None, primary_key=True)
    nome: str
    banco: Bancos = sqlmodel.Field(default=Bancos.NUBANK)
    tipo: str
    saldo: float
    usuario_id: int
    status: StatusConta = sqlmodel.Field(default=StatusConta.ATIVA)

    historicos: list["Historico"] = Relationship(back_populates="conta")

class Historico(sqlmodel.SQLModel, table=True):
    id: int = sqlmodel.Field(default=None, primary_key=True)
    conta_id: int = sqlmodel.Field(foreign_key="conta.id")
    
    tipo: Tipos = sqlmodel.Field(default=Tipos.ENTRADA)
    valor: float
    data: date

    conta: Conta = Relationship(back_populates="historicos")

    
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"    

engine = sqlmodel.create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    sqlmodel.SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    create_db_and_tables()    
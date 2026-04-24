from pydantic import BaseModel


class CriancaCreate(BaseModel):
    id: int
    nome: str
    idade: int
    responsavel: str


class CriancaOut(BaseModel):
    id: int
    nome: str
    idade: int
    responsavel: str

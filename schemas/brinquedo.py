from pydantic import BaseModel

class BrinquedoCreate(BaseModel):
    codigo: int
    nome: str
    categoria: str
    faixa_etaria_minima: int
    disponivel: bool = True

class BrinquedoOut(BaseModel):
    codigo: int
    nome: str
    categoria: str
    faixa_etaria_minima: int
    disponivel: bool

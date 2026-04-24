from pydantic import BaseModel


class BrinquedoCreate(BaseModel):
    id: int
    nome: str
    categoria: str
    faixa_etaria_minima: int
    disponivel: bool = True


class BrinquedoOut(BaseModel):
    id: int
    nome: str
    categoria: str
    faixa_etaria_minima: int
    disponivel: bool

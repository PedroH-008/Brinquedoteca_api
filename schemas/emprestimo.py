from datetime import date
from typing import Optional
from pydantic import BaseModel


class EmprestimoCreate(BaseModel):
    id: int
    crianca_id: int
    brinquedo_id: int
    data_emprestimo: date
    data_prevista_devolucao: date


class EmprestimoDevolucao(BaseModel):
    data_devolucao: Optional[date] = None


class EmprestimoOut(BaseModel):
    id: int
    crianca_id: int
    brinquedo_id: int
    data_emprestimo: date
    data_prevista_devolucao: date
    data_devolucao: Optional[date]
    status: str
    multa: float

from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Emprestimo:
    id: int
    crianca_id: int
    brinquedo_id: int
    data_emprestimo: date
    data_prevista_devolucao: date
    status: str = "ativo"
    data_devolucao: Optional[date] = None
    multa: float = 0.0

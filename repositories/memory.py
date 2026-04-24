from typing import Dict
from domain.brinquedo import Brinquedo
from domain.crianca import Crianca
from domain.emprestimo import Emprestimo

class MemoryDB:
    emprestimos_por_id: Dict[int, Emprestimo]
    criancas_por_id: Dict[int, Crianca]
    brinquedos_por_id: Dict[int, Brinquedo]

    def __init__(self):
        self.emprestimos_por_id: Dict[int, Emprestimo] = {}
        self.criancas_por_id: Dict[int, Crianca] = {}
        self.brinquedos_por_id: Dict[int, Brinquedo] = {}

db = MemoryDB()
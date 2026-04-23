from typing import Dict
from domain.brinquedo import Brinquedo
from domain.crianca import Crianca
from domain.emprestimo import Emprestimo

class MemoryDB():
    def __init__(self):
        self.Emprestimo_por_id: Dict[int, Emprestimo] = {}
        self.Crianca_por_id: Dict[int, Crianca] = {}
        self.Brinquedo_por_id: Dict[int, Brinquedo] = {}

db = MemoryDB()
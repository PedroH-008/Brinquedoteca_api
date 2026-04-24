from dataclasses import dataclass

@dataclass
class Crianca:
    id: int
    nome: str
    idade: int
    responsavel: str
    bloqueada: bool = False
    atrasos_acumulados: int = 0

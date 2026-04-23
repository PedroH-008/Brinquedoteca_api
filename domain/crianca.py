from dataclasses import dataclass

@dataclass(fronze=True)
class Crianca:
    id: int
    nome: str
    idade: int
    responsavel: str

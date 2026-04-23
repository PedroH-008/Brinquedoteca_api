from dataclasses import dataclass

@dataclass
class Brinquedo:
    id: int
    nome: str
    categoria: str
    faixa_etaria_minima: int
    disponivel: bool = True


def faixa(self, idade:int) -> int:
    if idade < faixa_etaria_minima:
        raise ValueError("Esta a baixo da Faixa Etaria")




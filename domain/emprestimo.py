from domain.brinquedo import Brinquedo
from domain.crianca import Crianca

class Emprestimo:
    def __init__(self, id: int, criança_id: Crianca, brinquedo_id: Brinquedo, datas: int, status: bool , multa: int):
        self.id: id
        self.criança_id: criança_id
        self.brinquedo_id: brinquedo_id
        self.datas: datas
        self.status: status
        self.multa: multa

    def __post_init__(self):
        if self.valor < 0:
            raise ValueError("Valor do produto não pode ser negativo")
        
        
    def multa(self, dt_final, dt_inicial, temp_entrega):
        if (dt_final - dt_inicial) > temp_entrega:
            self.multa += 2

        

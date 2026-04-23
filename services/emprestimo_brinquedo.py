from domain.brinquedo import Brinquedo
from domain.crianca import Crianca
#from domain.emprestimo import Emprestimo
from repositories.memory import db

class emprestimo_brinquedo:
    def criar_crianca(self, id: int,nome: str,idade: int,responsavel: str) -> Crianca:
        if id in db.Crianca_por_id:
            return db.Crianca_por_id[id]

        crianca = Crianca(id=id, nome=nome, idade=idade, responsavel=responsavel)
        db.Crianca_por_id[id] = crianca
        return crianca

    def obter_crianca(self, id: int) -> Crianca | None:
        return db.Crianca_por_id.get(id)

    def criar_brinquedo(self,id: int,nome: str,categoria: str,faixa_etaria_minima: int,disponivel: bool = True) -> Brinquedo:
        brinquedo = Brinquedo(id=id, nome=nome, categoria=categoria, faixa_etaria_minima=faixa_etaria_minima, disponivel=disponivel)
        db.Brinquedo_por_id[id] = brinquedo

    def obter_brinquedo(self, id: int) -> Brinquedo | None:
        return db.Brinquedo_por_id.get(id)
    

service = emprestimo_brinquedo()
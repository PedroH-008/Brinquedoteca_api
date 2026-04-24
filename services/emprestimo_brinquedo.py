from datetime import date
from domain.brinquedo import Brinquedo
from domain.crianca import Crianca
from domain.emprestimo import Emprestimo
from repositories.memory import db


class EmprestimoBrinquedoService:
    MULTA_DIARIA = 2.0
    MAX_EMPRESTIMOS_ATIVOS_POR_CRIANCA = 2
    ATRASOS_PARA_BLOQUEIO = 3

    def criar_crianca(self, id: int, nome: str, idade: int, responsavel: str) -> Crianca:
        if id in db.criancas_por_id:
            raise ValueError("Ja existe crianca com este id")

        if idade < 0:
            raise ValueError("Idade invalida")

        crianca = Crianca(id=id, nome=nome, idade=idade, responsavel=responsavel)
        db.criancas_por_id[id] = crianca
        return crianca

    def listar_criancas(self) -> list[Crianca]:
        return list(db.criancas_por_id.values())

    def obter_crianca(self, id: int) -> Crianca | None:
        return db.criancas_por_id.get(id)

    def criar_brinquedo(
        self,
        id: int,
        nome: str,
        categoria: str,
        faixa_etaria_minima: int,
        disponivel: bool = True,
    ) -> Brinquedo:
        if id in db.brinquedos_por_id:
            raise ValueError("Ja existe brinquedo com este id")

        if faixa_etaria_minima < 0:
            raise ValueError("Faixa etaria minima invalida")

        brinquedo = Brinquedo(
            id=id,
            nome=nome,
            categoria=categoria,
            faixa_etaria_minima=faixa_etaria_minima,
            disponivel=disponivel,
        )
        db.brinquedos_por_id[id] = brinquedo
        return brinquedo

    def listar_brinquedos(self) -> list[Brinquedo]:
        return list(db.brinquedos_por_id.values())

    def obter_brinquedo(self, id: int) -> Brinquedo | None:
        return db.brinquedos_por_id.get(id)

    def criar_emprestimo(
        self,
        id: int,
        crianca_id: int,
        brinquedo_id: int,
        data_emprestimo: date,
        data_prevista_devolucao: date,
    ) -> Emprestimo:
        if id in db.emprestimos_por_id:
            raise ValueError("Ja existe emprestimo com este id")

        crianca = self.obter_crianca(crianca_id)
        if not crianca:
            raise ValueError("Crianca nao encontrada")

        brinquedo = self.obter_brinquedo(brinquedo_id)
        if not brinquedo:
            raise ValueError("Brinquedo nao encontrado")

        if crianca.bloqueada:
            raise ValueError("Crianca bloqueada por recorrencia de atrasos")

        if data_prevista_devolucao < data_emprestimo:
            raise ValueError("Data prevista de devolucao nao pode ser menor que a data de emprestimo")

        if crianca.idade < brinquedo.faixa_etaria_minima:
            raise ValueError("Idade da crianca abaixo da faixa etaria minima do brinquedo")

        emprestimos_ativos_crianca = self._emprestimos_ativos_por_crianca(crianca_id)
        if len(emprestimos_ativos_crianca) >= self.MAX_EMPRESTIMOS_ATIVOS_POR_CRIANCA:
            raise ValueError("Crianca ja possui o maximo de 2 emprestimos ativos")

        if not brinquedo.disponivel:
            raise ValueError("Brinquedo indisponivel")

        if self._ha_conflito_de_horario(brinquedo_id, data_emprestimo, data_prevista_devolucao):
            raise ValueError("Conflito de horario para o brinquedo no periodo informado")

        emprestimo = Emprestimo(
            id=id,
            crianca_id=crianca_id,
            brinquedo_id=brinquedo_id,
            data_emprestimo=data_emprestimo,
            data_prevista_devolucao=data_prevista_devolucao,
        )

        db.emprestimos_por_id[id] = emprestimo
        brinquedo.disponivel = False
        return emprestimo

    def listar_emprestimos(self) -> list[Emprestimo]:
        return list(db.emprestimos_por_id.values())

    def obter_emprestimo(self, id: int) -> Emprestimo | None:
        return db.emprestimos_por_id.get(id)

    def listar_emprestimos_da_crianca(self, crianca_id: int) -> list[Emprestimo]:
        return [e for e in db.emprestimos_por_id.values() if e.crianca_id == crianca_id]

    def devolver_emprestimo(self, emprestimo_id: int, data_devolucao: date) -> Emprestimo:
        emprestimo = self.obter_emprestimo(emprestimo_id)
        if not emprestimo:
            raise ValueError("Emprestimo nao encontrado")

        if emprestimo.status != "ativo":
            raise ValueError("Emprestimo ja foi finalizado")

        if data_devolucao < emprestimo.data_emprestimo:
            raise ValueError("Data de devolucao nao pode ser menor que a data de emprestimo")

        atraso_em_dias = (data_devolucao - emprestimo.data_prevista_devolucao).days
        atraso_em_dias = max(atraso_em_dias, 0)

        emprestimo.data_devolucao = data_devolucao
        emprestimo.multa = atraso_em_dias * self.MULTA_DIARIA
        emprestimo.status = "devolvido_com_atraso" if atraso_em_dias > 0 else "devolvido"

        crianca = self.obter_crianca(emprestimo.crianca_id)
        if crianca and atraso_em_dias > 0:
            crianca.atrasos_acumulados += 1
            if crianca.atrasos_acumulados >= self.ATRASOS_PARA_BLOQUEIO:
                crianca.bloqueada = True

        brinquedo = self.obter_brinquedo(emprestimo.brinquedo_id)
        if brinquedo and not self._brinquedo_tem_emprestimo_ativo(brinquedo.id):
            brinquedo.disponivel = True

        return emprestimo

    def _emprestimos_ativos_por_crianca(self, crianca_id: int) -> list[Emprestimo]:
        return [
            emprestimo
            for emprestimo in db.emprestimos_por_id.values()
            if emprestimo.crianca_id == crianca_id and emprestimo.status == "ativo"
        ]

    def _brinquedo_tem_emprestimo_ativo(self, brinquedo_id: int) -> bool:
        return any(
            emprestimo.brinquedo_id == brinquedo_id and emprestimo.status == "ativo"
            for emprestimo in db.emprestimos_por_id.values()
        )

    def _ha_conflito_de_horario(
        self,
        brinquedo_id: int,
        data_inicio: date,
        data_fim: date,
    ) -> bool:
        for emprestimo in db.emprestimos_por_id.values():
            if emprestimo.brinquedo_id != brinquedo_id:
                continue

            if emprestimo.status != "ativo":
                continue

            inicio_existente = emprestimo.data_emprestimo
            fim_existente = emprestimo.data_prevista_devolucao
            ha_sobreposicao = data_inicio <= fim_existente and inicio_existente <= data_fim
            if ha_sobreposicao:
                return True

        return False


service = EmprestimoBrinquedoService()

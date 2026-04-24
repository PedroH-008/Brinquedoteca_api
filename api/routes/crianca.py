from fastapi import APIRouter, HTTPException
from schemas.crianca import CriancaCreate, CriancaOut
from schemas.emprestimo import EmprestimoOut
from services.emprestimo_brinquedo import service

router = APIRouter(prefix="/criancas", tags=["criancas"])

@router.post("", response_model=CriancaOut)
def criar(payload: CriancaCreate):
    try:
        crianca = service.criar_crianca(payload.id, payload.nome, payload.idade, payload.responsavel)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return CriancaOut(
        id=crianca.id,
        nome=crianca.nome,
        idade=crianca.idade,
        responsavel=crianca.responsavel,
    )


@router.get("", response_model=list[CriancaOut])
def listar():
    return [
        CriancaOut(
            id=crianca.id,
            nome=crianca.nome,
            idade=crianca.idade,
            responsavel=crianca.responsavel,
        )
        for crianca in service.listar_criancas()
    ]


@router.get("/{id}/emprestimos", response_model=list[EmprestimoOut])
def listar_emprestimos_da_crianca(id: int):
    crianca = service.obter_crianca(id)
    if not crianca:
        raise HTTPException(status_code=404, detail="Crianca nao encontrada")

    emprestimos = service.listar_emprestimos_da_crianca(id)
    return [
        EmprestimoOut(
            id=emprestimo.id,
            crianca_id=emprestimo.crianca_id,
            brinquedo_id=emprestimo.brinquedo_id,
            data_emprestimo=emprestimo.data_emprestimo,
            data_prevista_devolucao=emprestimo.data_prevista_devolucao,
            data_devolucao=emprestimo.data_devolucao,
            status=emprestimo.status,
            multa=emprestimo.multa,
        )
        for emprestimo in emprestimos
    ]
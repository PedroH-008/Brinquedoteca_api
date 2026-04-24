from datetime import date
from fastapi import APIRouter, HTTPException
from schemas.emprestimo import EmprestimoCreate, EmprestimoDevolucao, EmprestimoOut
from services.emprestimo_brinquedo import service


router = APIRouter(prefix="/emprestimos", tags=["emprestimos"])

@router.post("", response_model=EmprestimoOut)
def criar(payload: EmprestimoCreate):
    try:
        emprestimo = service.criar_emprestimo(
            payload.id,
            payload.crianca_id,
            payload.brinquedo_id,
            payload.data_emprestimo,
            payload.data_prevista_devolucao,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return EmprestimoOut(**emprestimo.__dict__)


@router.get("", response_model=list[EmprestimoOut])
def listar():
    return [EmprestimoOut(**emprestimo.__dict__) for emprestimo in service.listar_emprestimos()]


@router.get("/{id}", response_model=EmprestimoOut)
def obter(id: int):
    emprestimo = service.obter_emprestimo(id)
    if not emprestimo:
        raise HTTPException(status_code=404, detail="Emprestimo nao encontrado")

    return EmprestimoOut(**emprestimo.__dict__)


@router.put("/{id}/devolver", response_model=EmprestimoOut)
def devolver(id: int, payload: EmprestimoDevolucao):
    data_devolucao = payload.data_devolucao or date.today()

    try:
        emprestimo = service.devolver_emprestimo(id, data_devolucao)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return EmprestimoOut(**emprestimo.__dict__)

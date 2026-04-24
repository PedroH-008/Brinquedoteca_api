from fastapi import APIRouter, HTTPException
from schemas.brinquedo import BrinquedoCreate, BrinquedoOut
from services.emprestimo_brinquedo import service

router = APIRouter(prefix="/brinquedos", tags=["brinquedos"])

@router.post("", response_model=BrinquedoOut)
def criar(payload: BrinquedoCreate):
    try:
        brinquedo = service.criar_brinquedo(payload.id, payload.nome, payload.categoria, payload.faixa_etaria_minima, payload.disponivel)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return BrinquedoOut(**brinquedo.__dict__)


@router.get("", response_model=list[BrinquedoOut])
def listar():
    return [BrinquedoOut(**brinquedo.__dict__) for brinquedo in service.listar_brinquedos()]
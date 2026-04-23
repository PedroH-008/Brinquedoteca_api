from fastapi import APIRouter, HTTPException
from schemas.brinquedo import BrinquedoCreate, BrinquedoOut
from services.emprestimo_brinquedo import service

router = APIRouter(prefix="/brinquedo", tags=["brinquedo"])

@router.post("", response_model=BrinquedoOut)
def criar(payload: BrinquedoCreate):
    try:
        brinquedo = service.criar_brinquedo(payload.id, payload.nome, payload.categoria, payload.faixa_etaria_minima, payload.disponivel)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return BrinquedoOut(
        id=brinquedo.id,
        nome=brinquedo.nome, 
        categoria=brinquedo.categoria, 
        faixa_etaria_minima=brinquedo.faixa_etaria_minima, 
        disponivel=brinquedo.disponivel )

@router.get("/{id}", response_model=BrinquedoOut)
def obter(id: int):
    brinquedo = service.obter_brinquedo(id)
    if not brinquedo:
        raise HTTPException(
            status_code=404, 
            detail="Brinquedo não encontrado"
            )
    return BrinquedoOut(
        id=brinquedo.id, 
        nome=brinquedo.nome, 
        categoria=brinquedo.categoria, 
        faixa_etaria_minima=brinquedo.faixa_etaria_minima, 
        disponivel=brinquedo.disponivel )
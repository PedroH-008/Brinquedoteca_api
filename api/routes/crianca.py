from fastapi import APIRouter, HTTPException
from schemas.crianca import CriancaCreate, CriancaOut
from services.emprestimo_brinquedo import service

router = APIRouter(prefix="/crianca", tags=["criancas"])

@router.post("", response_model=CriancaOut)
def criar(payload: CriancaCreate):
    try:
        crianca = service.criar_crianca(payload.id, payload.nome, payload.idade, payload.responsavel)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return CriancaOut(id=crianca.id, nome=crianca.nome, idade=crianca.idade, responsavel=crianca.responsavel)

@router.get("/{id}", response_model=CriancaOut)
def obter(id: int):
    crianca = service.obter_crianca(id)
    if not crianca:
        raise HTTPException(
            status_code=404, 
            detail="Crianca não encontrado"
            )
    return CriancaOut(id=crianca.id, nome=crianca.nome, idade=crianca.idade, responsavel=crianca.responsavel)
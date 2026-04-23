from pydantic import BaseModel

class EmprestimoCreate(BaseModel):
    id: int
    crinca_id: int
    brinquedo_id: int
    datas: int
    status: bool = True
    multa: int

class EmprestimoOut(BaseModel):
    id: int
    crinca_id: int
    brinquedo_id: int
    datas: int
    status: bool
    multa: int
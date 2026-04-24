#import uvicorn
from fastapi import FastAPI
from api.routes.crianca import router as crianca_router
from api.routes.brinquedo import router as brinquedo_router
from api.routes.emprestimo import router as emprestimo_router

from fastapi.responses import JSONResponse
from fastapi import Request


app = FastAPI(
                title="Projeto Brinquedoteca", 
                description="API para emprestimo de brinquedo", 
                version="1.0.0"
            )

# Tratamento global de erros do tipo ValueError, retornando status 400 com a mensagem de erro
@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )

app.include_router(crianca_router)
app.include_router(brinquedo_router)
app.include_router(emprestimo_router)


#if __name__ == "__main__":
#    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
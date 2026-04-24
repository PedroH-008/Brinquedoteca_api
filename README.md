### Projeto Brinquedoteca API

### Instalar dependencias

pip install "fastapi[standard]"

### Executar o projeto

Desenvolvimento:
fastapi dev main.py

Producao:
fastapi run main.py

Alternativa com uvicorn:
uvicorn main:app --host 0.0.0.0 --port 8000

### Estrutura do projeto

domain/__init__.py

schemas/__init__.py

repositories/__init__.py

services/__init__.py

api/routes/__init__.py

main.py

### Regras de negocio

- Nao emprestar brinquedo indisponivel
- Validar idade da crianca para faixa etaria minima
- Maximo de 2 emprestimos ativos por crianca
- Multa de R$2 por dia de atraso
- Bloquear crianca apos 3 atrasos
- Validacao de conflito de horario para o mesmo brinquedo

### Endpoints minimos

POST /criancas
GET /criancas

POST /brinquedos
GET /brinquedos

POST /emprestimos
GET /emprestimos
GET /emprestimos/{id}
PUT /emprestimos/{id}/devolver

GET /criancas/{id}/emprestimos

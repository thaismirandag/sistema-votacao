
## Requisitos

- Python 3.11 ou superior
- Poetry

## Instalação

1. Instale o Poetry (caso ainda não tenha):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Instale as dependências do projeto:
```bash
poetry install
```

## Executando o projeto

Para iniciar o servidor de desenvolvimento:

```bash
poetry run uvicorn app.main:app --reload
```

A API estará disponível em `http://localhost:8000`

## Documentação

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints disponíveis

- `GET /`: Mensagem de boas-vindas
- `GET /health`: Verificação de saúde da API 
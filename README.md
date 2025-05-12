# Sistema de Votação

Sistema de votação utilizando FastAPI, PostgreSQL, Redis e Celery.

## Requisitos

- Docker
- Docker Compose
- Git

## Estrutura do Projeto

```
sistema-votacao/
├── backend/          # API FastAPI
├── frontend/         # Interface do usuário
├── architecture/     # Diagramas da arquitetura
└── docker-compose.yml
```

## Configuração do Ambiente

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd sistema-votacao
```

2. Configure as variáveis de ambiente:
```bash
cp backend/.env.example backend/.env
```
Edite o arquivo `.env` com suas configurações.

## Executando o Sistema

1. Inicie os containers:
```bash
docker-compose up -d
```

2. Execute as migrações do banco de dados:
```bash
docker-compose exec backend poetry run alembic upgrade head
```

3. Inicie o worker do Celery:
```bash
docker-compose exec backend poetry run celery -A app.core.celery_worker.celery_app worker --loglevel=info -Q votos -n votos.worker@%h
```

## Acessando o Sistema

- Frontend: http://localhost:3000
- API: http://localhost:8000
- Documentação da API: http://localhost:8000/docs
- Prometheus: http://localhost:9090

## Monitoramento

O sistema inclui monitoramento com Prometheus e métricas personalizadas:
- Taxa de votos por minuto
- Tempo de processamento
- Status do worker
- Cache hits/misses

## Desenvolvimento

### Backend

O backend é desenvolvido em Python usando:
- FastAPI para a API
- PostgreSQL para persistência
- Redis para cache e rate limiting
- Celery para processamento assíncrono
- Alembic para migrações

### Frontend

O frontend é desenvolvido em React e se comunica com o backend através da API REST.


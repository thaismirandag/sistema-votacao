# Sistema de Votação 

Sistema de votação desenvolvido com React/TypeScript no frontend e Python/FastAPI no backend.

## 📋 Documentação do Projeto

### Arquitetura

O sistema é composto por três componentes principais:

1. **Frontend (React/TypeScript)**
   - Interface web responsiva
   - Integração com reCAPTCHA
   - Exibição de resultados em tempo real
   - Estilização com styled-components

2. **Backend (Python/FastAPI)**
   - API REST
   - Validação de votos
   - Armazenamento em banco de dados
   - Rate limiting e proteção contra bots

3. **Monitoramento**
   - Prometheus para coleta de métricas
   - Grafana para visualização
   - Alertas configurados

### APIs

#### Endpoints Disponíveis

1. **GET /participantes**
   - Retorna lista de participantes no paredão
   - Resposta: `{ id: string, nome: string, foto_url: string, total_votos: number, percentual: number }[]`

2. **POST /votos**
   - Registra um novo voto
   - Body: `{ participante_id: string, captcha_token: string }`
   - Resposta: Status 200 em caso de sucesso

3. **GET /estatisticas**
   - Retorna estatísticas gerais
   - Resposta: `{ total_votos: number, votos_por_participante: { [id: string]: number }, votos_por_hora: { [hora: string]: number } }`

### Métricas

O sistema coleta as seguintes métricas em tempo real:

- Votos por segundo
- Taxa de sucesso/erro
- Tempo de resposta da API
- Uso de CPU/Memória
- Número de conexões ativas

## 🚀 Como Executar Localmente

### Pré-requisitos

- Docker
- Docker Compose
- Node.js 16+
- Python 3.8+

### Passos para Execução

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/sistema-votacao.git
cd sistema-votacao
```

2. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

3. Inicie os serviços:
```bash
docker-compose up -d
```

4. Acesse a aplicação:
- Frontend: http://localhost:3000
- API: http://localhost:8000
- Grafana: http://localhost:3001


## 📊 Plano de Trabalho

### Previsto
- [x] Desenvolvimento do frontend
- [x] Desenvolvimento do backend
- [x] Implementação do reCAPTCHA
- [x] Configuração do banco de dados
- [x] Testes de carga
- [ ] Implementação de métricas
- [ ] Configuração de CI/CD
- [ ] Documentação completa

### Realizado
- [x] Sistema básico de votação
- [x] Interface responsiva
- [x] Proteção contra bots
- [x] Armazenamento de votos
- [x] Testes de performance iniciais

## 🛠️ Tecnologias Utilizadas

- Frontend: React, TypeScript, styled-components
- Backend: Python, FastAPI
- Banco de Dados: PostgreSQL
- Cache: Redis
- Monitoramento: Prometheus, Grafana
- Containerização: Docker

## 🧠 Como funciona

- Os usuários acessam a interface e enviam votos através da API.
- O voto é validado com reCAPTCHA e armazenado temporariamente no Redis.
- O Celery processa os votos em segundo plano e grava no banco de dados (postgres).
- As métricas são expostas via Prometheus e visualizadas em dashboards Grafana.

## 📦 Estrutura do Projeto
- `architecture/`: Arquitetura do projeto
- `frontend/`: Código do frontend
- `backend/`: Código do backend
- `prometheus/`: Configuração do Prometheus
- `grafana/`: Configuração do Grafana
- `README.md`: Documentação do projeto
- `docker-compose.yml`: Configuração do Docker Compose



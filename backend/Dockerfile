# Imagem base
FROM python:3.11-slim

# Define o diretório de trabalho
WORKDIR /app

# Instala as dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instala o Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Adiciona o Poetry ao PATH
ENV PATH="/root/.local/bin:$PATH"

# Copia os arquivos de configuração
COPY pyproject.toml poetry.lock ./

# Configura o Poetry para não criar um ambiente virtual
RUN poetry config virtualenvs.create false

# Instala as dependências
RUN poetry install --no-interaction --no-ansi

# Copia o código fonte
COPY . .

# Expõe a porta que a aplicação usa
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 
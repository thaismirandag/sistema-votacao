FROM python:3.11-slim

RUN apt-get update && apt-get install -y curl build-essential && rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=1.8.2
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"
ENV POETRY_VIRTUALENVS_CREATE=false
WORKDIR /app
COPY pyproject.toml poetry.lock* /app/
RUN poetry install --no-root
COPY . /app
RUN poetry add gunicorn
CMD ["gunicorn", "app.main:app", "-k", "uvicorn.workers.UvicornWorker", "--workers", "4", "--bind", "0.0.0.0:8000"]

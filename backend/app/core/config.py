from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    PROJECT_NAME: str = "Sistema de Votação"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # Configurações do PostgreSQL
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "user"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "votacao"
    POSTGRES_PORT: str = "5432"
    
    # Configurações do Redis
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    
    # Configurações do reCAPTCHA
    RECAPTCHA_SITE_KEY: str = ""  
    RECAPTCHA_SECRET_KEY: str = ""  
    
    # Configurações de Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Configurações de Prometheus
    PROMETHEUS_MULTIPROC_DIR: str = "/tmp"
    
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    @property
    def REDIS_URL(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    class Config:
        case_sensitive = True
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings() 
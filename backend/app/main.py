from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.routers import voto as voto_router
from app.core.prometheus import setup_prometheus

settings = get_settings()

app = FastAPI(
    title="Sistema de Votação",
    description="",
    version="0.1.0"
    
)

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Inclui as rotas
app.include_router(voto_router.router, prefix="/api")

# Configura o Prometheus
setup_prometheus(app)




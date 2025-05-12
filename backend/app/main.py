from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import get_settings
from app.core.prometheus import setup_prometheus
from app.core.logging import setup_logging, log_error
from app.routers import voto as voto_router

settings = get_settings()

setup_logging()

app = FastAPI(
    title="Sistema de Votação",
    description="API para sistema de votação",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


setup_prometheus(app)

app.include_router(voto_router.router, prefix="/api")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    log_error(
        request_id=getattr(request.state, "request_id", "unknown"),
        error=exc,
        context={"path": request.url.path}
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Erro interno do servidor"}
    )

@app.on_event("startup")
async def startup_event():
    setup_prometheus(app)




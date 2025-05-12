
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.services.voto_service import VotoService

router = APIRouter()

@router.get("/metricas", response_model=dict)
async def get_metricas(
    db: Session = Depends()
) -> dict:
    """
    Retorna métricas gerais da votação.
    """
    voto_service = VotoService(db)
    return await voto_service.get_metricas()

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import Dict
from app.services.voto_service import VotoService

router = APIRouter()

@router.get("/metricas", response_model=Dict)
async def get_metricas(
    db: Session = Depends()
) -> Dict:
    """
    Retorna métricas gerais da votação.
    """
    voto_service = VotoService(db)
    return await voto_service.get_metricas() 
from fastapi import APIRouter, Depends
from app.services.voto_service import VotoService
from app.core.dependencies import get_voto_service

router = APIRouter()

@router.get("/metricas", response_model=dict)
async def get_metricas(
    service: VotoService = Depends(get_voto_service)
) -> dict:

    return await service.get_estatisticas()


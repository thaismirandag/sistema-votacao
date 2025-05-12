
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.voto import VotoCreate, VotoResponse
from app.services.voto import VotoService
from app.tasks import registrar_voto_task

router = APIRouter()


@router.post("/votar", response_model=VotoResponse)
async def votar(
    voto: VotoCreate,
    request: Request,
    db: Session = Depends(get_db)
) -> VotoResponse:
    """
    Registra um voto para um participante.
    Requer verificação de captcha.
    """
    # Obtém IP e User Agent do request
    ip_address = request.client.host
    user_agent = request.headers.get("user-agent")

    # Envia o voto para processamento assíncrono
    registrar_voto_task.delay(voto.dict(), ip_address, user_agent)

    # Obtém estatísticas atualizadas
    voto_service = VotoService(db)
    estatisticas = await voto_service.get_estatisticas()
    participante_stats = estatisticas["participantes"][voto.participante_id]

    return VotoResponse(
        participante_id=voto.participante_id,
        total_votos=participante_stats["total"],
        percentual=participante_stats["percentual"]
    )


@router.get("/estatisticas", response_model=dict)
async def get_estatisticas(
    db: Session = Depends(get_db)
) -> dict:
    """
    Retorna estatísticas gerais da votação.
    """
    voto_service = VotoService(db)
    return await voto_service.get_estatisticas()


from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from loguru import logger
from datetime import datetime

from app.core.database import get_db
from app.schemas.voto import VotoCreate, VotoResponse
from app.services.voto import VotoService
from app.tasks import registrar_voto_task
from app.core.prometheus import VOTOS_TOTAL

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
    request_id = getattr(request.state, "request_id", "unknown")
    logger.info(
        "Iniciando registro de voto",
        extra={
            "request_id": request_id,
            "participante_id": voto.participante_id
        }
    )

    try:
        ip_address = request.client.host
        user_agent = request.headers.get("user-agent")
        
        VOTOS_TOTAL.labels(participante_id=voto.participante_id).inc()

        voto_service = VotoService(db)
        hora_atual = datetime.now().strftime("%Y-%m-%d %H:00:00")
        chave_hora = f"votos:hora:{hora_atual}"
        chave_participante = f"votos:participante:{voto.participante_id}"
        
        voto_service.redis.incr(chave_hora)
        voto_service.redis.incr(chave_participante)

        task = registrar_voto_task.delay(voto.dict(), ip_address, user_agent)
        
        estatisticas = await voto_service.get_estatisticas()
        participante_stats = estatisticas["participantes"][voto.participante_id]

        logger.info(
            "Voto registrado com sucesso",
            extra={
                "request_id": request_id,
                "participante_id": voto.participante_id,
                "total_votos": participante_stats["total"],
                "percentual": participante_stats["percentual"]
            }
        )

        return VotoResponse(
            participante_id=voto.participante_id,
            total_votos=participante_stats["total"],
            percentual=participante_stats["percentual"]
        )

    except Exception as e:
        logger.error(
            "Erro ao registrar voto",
            extra={
                "request_id": request_id,
                "error": str(e)
            }
        )
        raise HTTPException(status_code=500, detail="Erro ao registrar voto")




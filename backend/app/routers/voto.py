from fastapi import APIRouter, Depends, Request, HTTPException
from loguru import logger
from datetime import datetime, timezone

from app.schemas.voto import VotoCreate, VotoResponse, VotoTesteCreate
from app.services.voto_service import VotoService
from app.tasks import registrar_voto_task
from app.core.prometheus import VOTOS_TOTAL
from app.services.captcha_service import CaptchaService
from app.core.dependencies import get_voto_service


router = APIRouter()


@router.post("/votacao", response_model=VotoResponse)
async def votar(
    voto: VotoCreate,
    request: Request,
    service: VotoService = Depends(get_voto_service)
) -> VotoResponse:
    """
    Registra um voto para um participante.
    Requer verificação de captcha.
    """
    request_id = getattr(request.state, "request_id", "unknown")
    logger.info("Iniciando registro de voto", extra={"request_id": request_id, "participante_id": voto.participante_id})

    try:
        await CaptchaService().verify_captcha(voto.captcha_token)

        ip_address = request.client.host
        user_agent = request.headers.get("user-agent")

        VOTOS_TOTAL.labels(participante_id=voto.participante_id).inc()

        hora_atual = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:00:00")
        await service.redis.incr(f"votos:hora:{hora_atual}")
        await service.redis.incr(f"votos:participante:{voto.participante_id}")

        registrar_voto_task.delay(voto.model_dump(), ip_address, user_agent)

        stats = await service.get_estatisticas()
        participante_stats = stats["participantes"][voto.participante_id]

        logger.info("Voto registrado com sucesso", extra={
            "request_id": request_id,
            "participante_id": voto.participante_id,
            "total_votos": participante_stats["total"],
            "percentual": participante_stats["percentual"]
        })

        return VotoResponse(
            participante_id=voto.participante_id,
            total_votos=participante_stats["total"],
            percentual=participante_stats["percentual"]
        )

    except Exception as e:
        logger.error("Erro ao registrar voto", extra={"request_id": request_id, "error": str(e)})
        raise HTTPException(status_code=500, detail=f"Erro ao registrar voto: {str(e)}")


@router.post("/teste/votacao", response_model=VotoResponse)
async def votar_teste(
    voto: VotoTesteCreate,
    request: Request,
    service: VotoService = Depends(get_voto_service)
) -> VotoResponse:
    """
    Endpoint de teste para votação.
    Bypass da validação do captcha.
    """
    request_id = getattr(request.state, "request_id", "unknown")
    logger.info("Iniciando registro de voto (teste)", extra={"request_id": request_id, "participante_id": voto.participante_id})

    try:
        ip_address = request.client.host
        user_agent = request.headers.get("user-agent")

        VOTOS_TOTAL.labels(participante_id=voto.participante_id).inc()

        db_voto = await service.registrar_voto(voto, ip_address, user_agent)

        stats = await service.get_estatisticas()
        participante_stats = stats["participantes"][voto.participante_id]

        logger.info("Voto registrado com sucesso (teste)", extra={
            "request_id": request_id,
            "participante_id": voto.participante_id,
            "total_votos": participante_stats["total"],
            "percentual": participante_stats["percentual"]
        })

        return VotoResponse(
            participante_id=voto.participante_id,
            total_votos=participante_stats["total"],
            percentual=participante_stats["percentual"]
        )

    except ValueError as ve:
        logger.error("Erro de validação ao registrar voto (teste)", extra={"request_id": request_id, "error": str(ve)})
        raise HTTPException(status_code=400, detail=str(ve))

    except Exception as e:
        logger.error("Erro ao registrar voto (teste)", extra={"request_id": request_id, "error": str(e)})
        raise HTTPException(status_code=500, detail=f"Erro ao registrar voto: {str(e)}")

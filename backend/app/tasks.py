import asyncio
from app.core.logging import logger
from app.core.celery_worker import celery_app
from app.core.database import async_session
from app.models.voto import Voto
from app.services.captcha_service import CaptchaService
from app.core.prometheus import VOTOS_TOTAL, ERROS_TOTAL
from redis.asyncio import Redis
from app.core.config import get_settings
from datetime import datetime, timezone

settings = get_settings()

@celery_app.task
def registrar_voto_task(voto_data: dict, ip_address: str, user_agent: str):
    asyncio.run(_registrar_voto(voto_data, ip_address, user_agent))

async def _registrar_voto(voto_data: dict, ip_address: str, user_agent: str):
    try:
        captcha_service = CaptchaService()
        await captcha_service.verify_captcha(voto_data["captcha_token"])

        session = async_session()
        try:
            voto = Voto(
                participante_id=voto_data["participante_id"],
                ip_address=ip_address,
                user_agent=user_agent
            )
            session.add(voto)
            await session.commit()
            await session.refresh(voto)

            # Atualiza métricas Redis
            redis = Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                decode_responses=True
            )
            hora_atual = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:00:00")
            await redis.incr(f"votos:hora:{hora_atual}")
            await redis.incr(f"votos:participante:{voto.participante_id}")
            await redis.close()

            VOTOS_TOTAL.labels(participante_id=voto.participante_id).inc()
            logger.info(f"Voto registrado com sucesso para participante {voto.participante_id}")
        finally:
            await session.close()

    except Exception as e:
        ERROS_TOTAL.labels(tipo_erro="celery_task").inc()
        logger.error(f"Erro ao registrar voto: {e}")
        raise

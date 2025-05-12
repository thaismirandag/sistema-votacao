from app.core.celery_worker import celery_app
from app.core.database import async_session
from app.models.voto import Voto
from app.services.captcha_service import CaptchaService


@celery_app.task
async def registrar_voto_task(voto_data: dict, ip_address: str, user_agent: str):
    # Verifica o captcha
    captcha_service = CaptchaService()
    await captcha_service.verify_captcha(voto_data["captcha_token"])

    # Registra o voto no banco
    async with async_session() as db:
        try:
            voto = Voto(
                participante_id=voto_data["participante_id"],
                ip_address=ip_address,
                user_agent=user_agent
            )
            db.add(voto)
            await db.commit()
        except Exception:
            await db.rollback()
            raise

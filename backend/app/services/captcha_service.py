import httpx
from fastapi import HTTPException

from app.core.config import get_settings

settings = get_settings()


class CaptchaError(Exception):
    pass


class CaptchaService:
    def __init__(self):
        self.verify_url = "https://www.google.com/recaptcha/api/siteverify"
        self.secret_key = settings.RECAPTCHA_SECRET_KEY

    async def verify_captcha(self, token: str) -> bool:

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.verify_url,
                    data={
                        "secret": self.secret_key,
                        "response": token
                    }
                )

                result = response.json()

                if not result.get("success", False):
                    raise HTTPException(
                        status_code=400,
                        detail="Captcha inválido"
                    )

                return True

        except Exception as err:
            raise CaptchaError("Erro ao validar captcha") from err

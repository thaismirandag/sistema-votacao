from datetime import datetime, timedelta

from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.models.voto import Voto
from app.schemas.voto import VotoCreate

settings = get_settings()


class VotoService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.redis = Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True
        )

    async def registrar_voto(self, voto: VotoCreate, ip_address: str, user_agent: str) -> Voto:
        hora_atual = datetime.now().strftime("%Y-%m-%d %H:00:00")
        chave_hora = f"votos:hora:{hora_atual}"
        chave_participante = f"votos:participante:{voto.participante_id}"

        self.redis.incr(chave_hora)
        self.redis.incr(chave_participante)

        db_voto = Voto(
            participante_id=voto.participante_id,
            ip_address=ip_address,
            user_agent=user_agent
        )
        self.db.add(db_voto)
        await self.db.commit()
        await self.db.refresh(db_voto)

        return db_voto

    async def get_estatisticas(self) -> dict:
        total_votos = sum(int(self.redis.get(f"votos:participante:{pid}") or 0)
                         for pid in range(1, 3))

        estatisticas = {
            "total_geral": total_votos,
            "participantes": {},
            "votos_por_hora": {}
        }

        for pid in range(1, 3):
            votos = int(self.redis.get(f"votos:participante:{pid}") or 0)
            percentual = (votos / total_votos * 100) if total_votos > 0 else 0
            estatisticas["participantes"][pid] = {
                "total": votos,
                "percentual": round(percentual, 2)
            }

        for i in range(24):
            hora = (datetime.now() - timedelta(hours=i)).strftime("%Y-%m-%d %H:00:00")
            votos_hora = int(self.redis.get(f"votos:hora:{hora}") or 0)
            estatisticas["votos_por_hora"][hora] = votos_hora

        return estatisticas

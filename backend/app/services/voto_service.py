from datetime import datetime, timezone, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis, RedisError
from app.models.voto import Voto
from app.schemas.voto import VotoCreate
from app.core.logging import logger
from sqlalchemy import select
from app.models.participante import Participante

class VotoService:
    def __init__(self, db: AsyncSession, redis: Redis):
        self.db = db
        self.redis = redis

    async def registrar_voto(self, voto: VotoCreate, ip_address: str, user_agent: str) -> Voto:
        hora_atual = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:00:00")
        chave_hora = f"votos:hora:{hora_atual}"
        chave_participante = f"votos:participante:{voto.participante_id}"

        try:
            await self.redis.incr(chave_hora)
            await self.redis.incr(chave_participante)
        except RedisError as redis_err:
            logger.warning(
                f"Não foi possível atualizar métricas Redis para voto de {voto.participante_id}: {redis_err}"
            )

        try:
            db_voto = Voto(
                participante_id=voto.participante_id,
                ip_address=ip_address,
                user_agent=user_agent
            )
            self.db.add(db_voto)
            await self.db.flush()
            await self.db.refresh(db_voto)
            await self.db.commit()
            return db_voto
        except Exception as e:
            if self.db.is_active:
                await self.db.rollback()
            raise e

    async def get_estatisticas(self) -> dict:
        try:
            result = await self.db.execute(select(Participante.id))
            participantes_ids = result.scalars().all()

            estatisticas = {
                "total_geral": 0,
                "participantes": {},
                "votos_por_hora": {}
            }

            votos_por_participante = {}
            total_votos = 0

            for pid in participantes_ids:
                chave = f"votos:participante:{pid}"
                try:
                    votos = int(await self.redis.get(chave) or 0)
                except RedisError as e:
                    logger.warning(f"Erro ao acessar Redis para participante {pid}: {e}")
                    votos = 0
                votos_por_participante[pid] = votos
                total_votos += votos

            estatisticas["total_geral"] = total_votos

            for pid in participantes_ids:
                votos = votos_por_participante[pid]
                percentual = round((votos / total_votos * 100), 2) if total_votos else 0
                estatisticas["participantes"][str(pid)] = {
                    "total": votos,
                    "percentual": percentual
                }

            # Gera estatísticas por hora (últimas 24h)
            for i in range(24):
                hora = (datetime.now(timezone.utc) - timedelta(hours=i)).strftime("%Y-%m-%d %H:00:00")
                try:
                    votos_hora = int(await self.redis.get(f"votos:hora:{hora}") or 0)
                except RedisError as e:
                    logger.warning(f"Erro ao acessar Redis para hora {hora}: {e}")
                    votos_hora = 0
                estatisticas["votos_por_hora"][hora] = votos_hora

            return estatisticas

        except Exception as e:
            logger.error(f"Erro ao calcular estatísticas: {e}")
            raise
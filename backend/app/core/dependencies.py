from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from app.core.database import get_db
from app.services.voto_service import VotoService
from app.core.config import get_settings

settings = get_settings()

async def get_voto_service(db: AsyncSession = Depends(get_db)) -> VotoService:
    redis = Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        decode_responses=True
    )
    try:
        service = VotoService(db=db, redis=redis)
        yield service
    finally:
        await redis.close()

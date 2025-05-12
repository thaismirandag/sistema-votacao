

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.core.config import get_settings

settings = get_settings()

class Base(DeclarativeBase):
    pass

# Atualiza a URL do banco para usar o driver asyncpg
database_url = settings.SQLALCHEMY_DATABASE_URI.replace('postgresql://', 'postgresql+asyncpg://')

engine = create_async_engine(
    database_url,
    echo=False,
)

async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

async def get_db() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import get_settings

# Initialize settings
settings = get_settings()


# Base declaration
class Base(DeclarativeBase):
    pass

# Configuração do engine com pool de conexões
engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI.replace("postgresql://", "postgresql+asyncpg://"),
    echo=True,
)

# Configuração da sessão assíncrona
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

@asynccontextmanager
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency para obter uma sessão do banco de dados.
    Garante que a sessão seja fechada após o uso.
    """
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


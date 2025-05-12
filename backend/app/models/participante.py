from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

from app.core.database import Base


class Participante(Base):
    __tablename__ = "participantes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    foto_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

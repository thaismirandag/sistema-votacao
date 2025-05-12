from sqlalchemy import Column, DateTime, String
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.core.database import Base


class Participante(Base):
    __tablename__ = "participantes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    nome = Column(String, nullable=False)
    foto_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

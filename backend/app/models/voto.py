from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID  
import uuid

from app.core.database import Base

class Voto(Base):
    __tablename__ = "votos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    participante_id = Column(UUID(as_uuid=True), ForeignKey("participantes.id"), nullable=False)
    ip_address = Column(String, nullable=False)
    user_agent = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

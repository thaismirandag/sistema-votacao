from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import uuid

class ParticipanteBase(BaseModel):
    nome: str
    foto_url: Optional[str] = None


class ParticipanteCreate(ParticipanteBase):
    pass


class ParticipanteInDB(ParticipanteBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ParticipanteResponse(ParticipanteInDB):
    total_votos: int = 0
    percentual: float = 0.0 
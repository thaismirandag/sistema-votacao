import uuid
from datetime import datetime

from pydantic import BaseModel


class ParticipanteBase(BaseModel):
    nome: str
    foto_url: str | None = None


class ParticipanteCreate(ParticipanteBase):
    pass


class ParticipanteInDB(ParticipanteBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class ParticipanteResponse(ParticipanteInDB):
    total_votos: int = 0
    percentual: float = 0.0

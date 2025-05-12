from datetime import datetime
from uuid import UUID
from typing import Optional
from pydantic import BaseModel, ConfigDict


class ParticipanteBase(BaseModel):
    nome: str
    foto_url: Optional[str] = None


class ParticipanteCreate(ParticipanteBase):
    pass


class ParticipanteInDB(ParticipanteBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class ParticipanteResponse(ParticipanteInDB):
    total_votos: int = 0
    percentual: float = 0.0


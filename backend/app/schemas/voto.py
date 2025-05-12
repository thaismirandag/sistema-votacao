from datetime import datetime
from uuid import UUID
from typing import Optional
from pydantic import BaseModel, ConfigDict


class VotoBase(BaseModel):
    participante_id: str
    captcha_token: str


class VotoCreate(VotoBase):
    pass


class VotoTesteCreate(BaseModel):
    participante_id: str


class VotoInDB(VotoBase):
    id: UUID
    ip_address: str
    user_agent: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class VotoResponse(BaseModel):
    participante_id: str
    total_votos: int
    percentual: float

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class VotoBase(BaseModel):
    participante_id: int
    captcha_token: str  


class VotoCreate(VotoBase):
    pass


class VotoInDB(VotoBase):
    id: int
    ip_address: str
    user_agent: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class VotoResponse(BaseModel):
    participante_id: int
    total_votos: int
    percentual: float

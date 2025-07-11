from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class JobDescriptionBase(BaseModel):
    title: str
    description: str
    location: str
    skills: str
    experience: str
    education: str
    application_limit: Optional[int] = 20

class JobDescriptionCreate(JobDescriptionBase):
    user_id: UUID

class JobDescriptionUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    skills: Optional[str] = None
    experience: Optional[str] = None
    education: Optional[str] = None
    application_limit: Optional[int] = None

    
class JobDescriptionResponse(JobDescriptionBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

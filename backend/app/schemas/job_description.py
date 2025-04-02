from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class JobDescriptionBase(BaseModel):
    title: str
    description: str
    location: str
    skills: str
    experience: str
    education: str

class JobDescriptionCreate(JobDescriptionBase):
    user_id: UUID

class JobDescriptionUpdate(JobDescriptionBase):
    pass

class JobDescriptionResponse(JobDescriptionBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True

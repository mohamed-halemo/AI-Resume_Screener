from pydantic import BaseModel, HttpUrl, EmailStr
from uuid import UUID
from typing import Optional

class PersonalInfoBase(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    linkedin: Optional[HttpUrl] = None
    github: Optional[HttpUrl] = None
    website: Optional[HttpUrl] = None

class PersonalInfoCreate(PersonalInfoBase):
    resume_id: UUID

class PersonalInfoUpdate(PersonalInfoBase):
    pass

class PersonalInfoResponse(PersonalInfoBase):
    id: UUID
    resume_id: UUID

    class Config:
        orm_mode = True

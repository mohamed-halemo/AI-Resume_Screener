from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class PersonalInfoBase(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    website: Optional[str] = None

class PersonalInfoCreate(PersonalInfoBase):
    resume_id: UUID

class PersonalInfoUpdate(PersonalInfoBase):
    pass

class PersonalInfoResponse(PersonalInfoBase):
    id: UUID
    resume_id: UUID

    class Config:
        from_attributes = True

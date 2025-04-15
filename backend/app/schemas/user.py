 
from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from typing import Literal

class UserBase(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Literal["Admin", "applicant", "HR"]

class UserCreate(UserBase):
    id: UUID=None
  


class UserUpdate(UserBase):
    pass

class UserResponse(UserBase):
    id: UUID
    created_at: datetime


    class Config:
        from_attributes = True

    

 
from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from typing import Literal,Optional

class UserBase(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Literal["Admin", "applicant", "HR"]



class UserCreate(UserBase):
    id: Optional[UUID]=None
  


class UserUpdate(UserBase):
    pass

class UserResponse(UserBase):
    id: UUID
    created_at: datetime


    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


    
# We will return token along with the user data in response
class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    created_at: datetime


class UserDetails(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    role: Literal["Admin", "applicant", "HR"]
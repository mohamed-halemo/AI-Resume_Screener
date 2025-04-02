from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class ResumeBase(BaseModel):
    objective: Optional[str] = None
    skills: Optional[str] = None
    experience: Optional[str] = None
    education: Optional[str] = None
    location: Optional[str] = None
    certifications: Optional[str] = None
    projects: Optional[str] = None
    languages: Optional[str] = None
    publications: Optional[str] = None
    volunteer_experience: Optional[str] = None
    awards: Optional[str] = None
    references: Optional[str] = None
    parsed_text: Optional[str] = None

class ResumeCreate(ResumeBase):
    user_id: UUID

class ResumeUpdate(ResumeBase):
    pass

class ResumeResponse(ResumeBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    ai_feedback: Optional[AIFeedbackResponse] = None
    personal_info: Optional[PersonalInfoResponse] = None

    class Config:
        orm_mode = True


from schemas.ai_feedback import AIFeedbackResponse
from schemas.personal_info import PersonalInfoResponse
ResumeResponse.model_rebuild()
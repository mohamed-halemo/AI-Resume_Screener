 
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class AIFeedbackBase(BaseModel):
    feedback_text: str

class AIFeedbackCreate(AIFeedbackBase):
    resume_id: UUID

class AIFeedbackUpdate(AIFeedbackBase):
    pass

class AIFeedbackResponse(AIFeedbackBase):
    id: UUID
    resume_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

from backend.app.schemas.resume import ResumeResponse
AIFeedbackResponse.model_rebuild()


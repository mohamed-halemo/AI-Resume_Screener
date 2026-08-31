from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class ResumeJobLinkBase(BaseModel):
    is_matched: bool = False
    score: Optional[float] = None
    ranking: Optional[int] = None

class ResumeJobLinkCreate(ResumeJobLinkBase):
    resume_id: UUID
    job_id: UUID

class ResumeJobLinkUpdate(ResumeJobLinkBase):
    pass

class ResumeJobLinkResponse(ResumeJobLinkBase):
    id: UUID
    resume_id: UUID
    job_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

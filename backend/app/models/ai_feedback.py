 
from sqlalchemy import Column, Text, UUID, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from backend.app.core.database import Base
from sqlalchemy.sql import func
import uuid


class AIFeedback(Base):
    __tablename__ = "ai_feedback"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)  # UUID primary key
    resume_id = Column(UUID(as_uuid=True), ForeignKey("resumes.id", ondelete='CASCADE'), nullable=False)  # Use UUID for foreign key
    feedback_text = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    resume = relationship("Resume", back_populates="ai_feedback")

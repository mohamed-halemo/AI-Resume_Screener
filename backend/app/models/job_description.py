from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP,Text,UUID
from sqlalchemy.orm import relationship
from backend.app.core.database import Base
from sqlalchemy.sql import func
import uuid

class JobDescription(Base):
    __tablename__ = "job_descriptions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True) 
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    location = Column(Text, nullable=False)
    skills = Column(Text, nullable=False)
    experience = Column(Text, nullable=False)
    education = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="job_descriptions")
    resume_links = relationship("ResumeJobLink", back_populates="job")

from sqlalchemy import Column, Integer, UUID, ForeignKey, TIMESTAMP,Text
from sqlalchemy.orm import relationship
from backend.app.core.database import Base
from sqlalchemy.sql import func
import uuid
from backend.app.models.personal_info import PersonalInfo
from backend.app.models.ai_feedback import AIFeedback

class Resume(Base):
    __tablename__ = "resumes"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True) 
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Core resume details
    objective= Column(Text, nullable=True)
    skills = Column(Text, nullable=True)
    experience = Column(Text, nullable=True)
    education = Column(Text, nullable=True)
    location = Column(Text, nullable=True)
    certifications = Column(Text, nullable=True)
    projects = Column(Text, nullable=True)
    languages = Column(Text, nullable=True)
    publications = Column(Text, nullable=True)
    volunteer_experience = Column(Text, nullable=True)
    awards = Column(Text, nullable=True)
    references = Column(Text, nullable=True)
    
    # AI feedback & parsing info
    parsed_text = Column(Text, nullable=True)
    ai_feedback = relationship("AIFeedback", back_populates="resume", uselist=False,passive_deletes=True)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="resume")
    resume_job_links = relationship("ResumeJobLink", back_populates="resume")
    
    # One-to-One relationship to PersonalInfo
    personal_info = relationship("PersonalInfo", back_populates="resume", uselist=False,passive_deletes=True)  # One-to-One

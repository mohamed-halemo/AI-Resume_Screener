 
from sqlalchemy import Column, Integer, UUID, ForeignKey, TIMESTAMP,Boolean,Float
from sqlalchemy.orm import relationship
from backend.app.core.database import Base
from sqlalchemy.sql import func
import uuid


class ResumeJobLink(Base):
    __tablename__ = "resume_job_links"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)  # UUID primary key
    resume_id = Column(UUID(as_uuid=True), ForeignKey("resumes.id"), nullable=False)  # Use UUID for foreign key
    job_id = Column(UUID(as_uuid=True), ForeignKey("job_descriptions.id"), nullable=False)  # Use UUID for foreign key
    is_matched = Column(Boolean, default=False)
    score = Column(Float, nullable=True)
    ranking = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    resume = relationship("Resume", back_populates="resume_job_links")
    job = relationship("JobDescription", back_populates="resume_links")

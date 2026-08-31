from sqlalchemy import Column, Integer, UUID, ForeignKey, TIMESTAMP,Text
from sqlalchemy.orm import relationship
from backend.app.core.database import Base
from sqlalchemy.sql import func
import uuid



class PersonalInfo(Base):
    __tablename__ = "personal_info"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)  # UUID primary key
    resume_id = Column(UUID(as_uuid=True), ForeignKey("resumes.id", ondelete='CASCADE'), nullable=False)  # Foreign key to Resume
    name = Column(Text, nullable=False)  # Personal info fields
    email = Column(Text, nullable=True)
    phone = Column(Text, nullable=True)
    address = Column(Text, nullable=True)
    linkedin = Column(Text, nullable=True)
    github = Column(Text, nullable=True)
    website = Column(Text, nullable=True)

    resume = relationship("Resume", back_populates="personal_info", uselist=False)  # One-to-One relationship

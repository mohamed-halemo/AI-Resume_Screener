

from sqlalchemy import Column, UUID, String,TIMESTAMP
from sqlalchemy.orm import relationship
from backend.app.core.database import Base
from sqlalchemy.sql import func
import uuid

class User(Base):
    __tablename__ = "users"

    # Role choices
    ADMIN = "Admin"
    CANDIDATE = "Candidate"
    HR = "HR"
    ROLE_CHOICES = [(ADMIN, "Admin"), (CANDIDATE, "Candidate"), (HR, "HR")]


    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True) 
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, unique=False, nullable=False)
    role = Column(String, nullable=False,default=CANDIDATE)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    job_descriptions = relationship("JobDescription", back_populates="user", cascade="all, delete-orphan")
    resume = relationship("Resume", back_populates="user", uselist=False)  # One-to-One relationship


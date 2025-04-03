from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.job_description import JobDescription
from app.schemas.job_description import JobDescriptionCreate

router = APIRouter()

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint to upload a new job description
@router.post("/upload_job_description", response_model=JobDescriptionCreate)
def upload_job_description(job_description: JobDescriptionCreate, db: Session = Depends(get_db)):
    db_job_description = JobDescription(
        title=job_description.title,
        description=job_description.description,
        location=job_description.location,
        skills=job_description.skills,
        experience=job_description.experience,
        education=job_description.education
    )
    db.add(db_job_description)
    db.commit()
    db.refresh(db_job_description)
    return db_job_description

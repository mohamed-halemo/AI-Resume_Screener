
from sqlalchemy.orm import Session
from backend.app.models.job_description import JobDescription
from backend.app.schemas.job_description import JobDescriptionCreate
from backend.app.schemas.job_description import JobDescriptionUpdate
from fastapi import HTTPException
from uuid import UUID

def create_job_description(data: JobDescriptionCreate, db: Session):
    job = JobDescription(**data.model_dump())
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

def get_all_job_descriptions(db: Session):
    return db.query(JobDescription).all()

def get_job_description(job_id: UUID, db: Session):
    job = db.query(JobDescription).filter(JobDescription.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

def update_job_description(job_id: UUID, data: JobDescriptionCreate, db: Session):
    job = db.query(JobDescription).filter(JobDescription.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    for field, value in data.model_dump().items():
        setattr(job, field, value)
    db.commit()
    db.refresh(job)
    return job

def partial_update_job_description(job_id: UUID, data: JobDescriptionUpdate, db: Session):
    job = db.query(JobDescription).filter(JobDescription.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(job, field, value)
    
    db.commit()
    db.refresh(job)
    return job

def delete_job_description(job_id: UUID, db: Session):
    job = db.query(JobDescription).filter(JobDescription.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if job.resume_links:
        for link in job.resume_links:
            db.delete(link)


    db.delete(job)
    db.commit()
    return {"message": "Job deleted successfully"}
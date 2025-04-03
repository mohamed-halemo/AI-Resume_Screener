from sqlalchemy.orm import Session
from backend.app.models.job_description import JobDescription
from backend.app.schemas.job_description import JobDescriptionCreate

def create_job_description(job_description: JobDescriptionCreate, db: Session):
    db_job_description = JobDescription(
        title=job_description.title,
        description=job_description.description,
        location=job_description.location,
        skills=job_description.skills,
        experience=job_description.experience,
        education=job_description.education,
        user_id=job_description.user_id
    )
    db.add(db_job_description)
    db.commit()
    db.refresh(db_job_description)
    return db_job_description

from fastapi import APIRouter, Depends,status
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.schemas.job_description import JobDescriptionCreate
from backend.app.services.job_description_service import create_job_description

router = APIRouter()

@router.post("", response_model=JobDescriptionCreate, status_code=status.HTTP_201_CREATED)
def upload_job_description(job_description: JobDescriptionCreate, db: Session = Depends(get_db)):
    return create_job_description(job_description, db)

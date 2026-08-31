

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from backend.app.core.database import get_db
from backend.app.schemas import job_description as job_schemas
from backend.app.services import job_description_service
from backend.app.models.user import User
from backend.app.services.user_service import require_role

router = APIRouter(tags=["Job Description"])


@router.post("/job-descriptions", response_model=job_schemas.JobDescriptionResponse, status_code=status.HTTP_201_CREATED)
def upload_job_description(
    job_description: job_schemas.JobDescriptionCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("HR","Admin"))
):
    return job_description_service.create_job_description(job_description, db)


@router.get("/job-descriptions", response_model=List[job_schemas.JobDescriptionResponse])
def list_job_descriptions(
    db: Session = Depends(get_db),
    user: User = Depends(require_role("applicant","Admin"))
):
    return job_description_service.get_all_job_descriptions(db)


@router.get("/job-descriptions/{job_id}", response_model=job_schemas.JobDescriptionResponse)
def get_job_description(
    job_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("HR","Admin"))
):
    return job_description_service.get_job_description(job_id, db)


@router.put("/job-descriptions/{job_id}", response_model=job_schemas.JobDescriptionResponse)
def update_job_description(
    job_id: UUID,
    job_description: job_schemas.JobDescriptionCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("HR","Admin"))
):
    return job_description_service.update_job_description(job_id, job_description, db)


@router.patch("/job-descriptions/{job_id}", response_model=job_schemas.JobDescriptionResponse)
def partial_update_job_description(
    job_id: UUID,
    job_description: job_schemas.JobDescriptionUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("HR", "Admin"))
):
    return job_description_service.partial_update_job_description(job_id, job_description, db)


@router.delete("/job-descriptions/{job_id}")
def delete_job_description(
    job_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("HR","Admin"))
):
    return job_description_service.delete_job_description(job_id, db)

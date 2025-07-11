
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.services.resume_job_link_service import ResumeJobLinkService
from backend.app.services.user_service import get_current_user, require_role
from backend.app.models.user import User
from uuid import UUID

router = APIRouter(prefix="/resume-job-link", tags=["Resume Job Link"])

@router.post("/link")
def link_resume_to_job(
    resume_id: UUID,
    job_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("applicant","Admin"))
):
    service = ResumeJobLinkService(db)
    return service.link_resume_to_job(resume_id=resume_id, job_id=job_id)


@router.delete("/unlink")
def unlink_resume_from_job(
    resume_id: UUID,
    job_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("applicant", "Admin"))
):
    service = ResumeJobLinkService(db)
    return service.unlink_resume_from_job(resume_id, job_id)

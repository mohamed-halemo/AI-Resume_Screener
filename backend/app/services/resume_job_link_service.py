
from sqlalchemy.orm import Session
from backend.app.models.resume_job_link import ResumeJobLink
from backend.app.models.job_description import JobDescription
from fastapi import HTTPException
from uuid import UUID

#TODO: handle job description status and links when the job is closed/ applicants received there feedbacks.
#TODO: handle view/view-matched processes for job-resumes links from HR/Admin prespectives


class ResumeJobLinkService:
    def __init__(self, db: Session):
        self.db = db

    def link_resume_to_job(self, resume_id: UUID, job_id: UUID):
        job = self.db.query(JobDescription).filter(JobDescription.id == job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")

        count = self.db.query(ResumeJobLink).filter(ResumeJobLink.job_id == job_id).count()

        if count >= job.application_limit:

            #TODO: ALgorithm for looping on cvs for filter and give feedbacks (AI)
            return {
                "message": "Application limit reached. resumes will be processed by AI for filtering and feedback."
            }

        # Check if already linked
        existing = self.db.query(ResumeJobLink).filter_by(resume_id=resume_id, job_id=job_id).first()
        if existing:
            return {"message": "Already applied to this job."}

        link = ResumeJobLink(resume_id=resume_id, job_id=job_id)
        self.db.add(link)
        self.db.commit()
        return {"message": "Resume linked to job successfully", "job_id": str(job_id)}
    
    def unlink_resume_from_job(self, resume_id: UUID, job_id: UUID):
        link = self.db.query(ResumeJobLink).filter_by(resume_id=resume_id, job_id=job_id).first()
        if not link:
            raise HTTPException(status_code=404, detail="Resume is not linked to this job")
        
        self.db.delete(link)
        self.db.commit()
        return {"message": "Resume unlinked from job successfully"}


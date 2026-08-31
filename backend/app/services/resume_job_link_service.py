
from sqlalchemy.orm import Session
from backend.app.models.resume_job_link import ResumeJobLink
from backend.app.models.ai_feedback import AIFeedback
from backend.app.models.job_description import JobDescription
from fastapi import HTTPException
from uuid import UUID
from services.resume_ranker_service import ResumeRanker   # import your ranking class

#TODO: handle job description status and links when the job is closed/ applicants received there feedbacks.
#TODO: handle view/view-matched processes for job-resumes links from HR/Admin prespectives


class ResumeJobLinkService:
    def __init__(self, db: Session):
        self.db = db
        self.ranker = ResumeRanker()  

    def link_resume_to_job(self, resume_id: UUID, job_id: UUID):
        job = self.db.query(JobDescription).filter(JobDescription.id == job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")

        if job.status=="closed":
            raise HTTPException(status_code=403, detail="This job is closed for new applications.")

        count = self.db.query(ResumeJobLink).filter(ResumeJobLink.job_id == job_id).count()


        if count >= job.application_limit:
            #  Automatically close the job when limit is reached
            job.status = "closed"
            self.db.commit()            
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
    
    #  HR/Admin: View all resumes for a given job

    def get_all_resumes_for_job(self, job_id: UUID):
        job = self.db.query(JobDescription).filter(JobDescription.id == job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")

        links = self.db.query(ResumeJobLink).filter(ResumeJobLink.job_id == job_id).all()
        return links

    #view all matched resumes
    def update_matched_resumes_for_job(self, job_id: UUID, threshold: float = 0.5):
        job = self.db.query(JobDescription).filter(JobDescription.id == job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")

        links = self.db.query(ResumeJobLink).filter(ResumeJobLink.job_id == job_id).all()

        ranked = []
        for link in links:
            resume = link.resume
            if not resume:
                continue

            job_dict = {
                "description": job.description,
                "skills": job.skills,
                "experience": job.experience,
                "education": job.education,
                "location": job.location,
            }

            resume_dict = {
                "objective": resume.objective,
                "skills": resume.skills,
                "experience": resume.experience,
                "education": resume.education,
                "location": resume.location,
                "projects": resume.projects,
            }

            score, details = self.ranker.rank_resume(job_dict, resume_dict)

            ranked.append((link, score))

        # Sort by score descending
        ranked.sort(key=lambda x: x[1], reverse=True)

        # Update each ResumeJobLink
        for rank, (link, score) in enumerate(ranked, start=1):
            link.score = score
            link.ranking = rank
            link.is_matched = score >= threshold  # mark as matched only if score exceeds threshold

        self.db.commit()
        return {"updated": len(ranked)}


def generate_and_save_ai_feedback(self, resume_id: UUID, job_id: UUID) -> AIFeedback:
    link = (
        self.db.query(ResumeJobLink)
        .filter(
            ResumeJobLink.resume_id == resume_id,
            ResumeJobLink.job_id == job_id
        )
        .first()
    )
    if not link:
        raise HTTPException(status_code=404, detail="Match info not found")

    # Generate basic feedback based on matching results
    if link.is_matched:
        feedback_text = (
            f"Your resume matched the job with a score of {link.score:.2f}. "
            f"You're ranked #{link.ranking}. Strong alignment detected!"
        )
    else:
        feedback_text = (
            f" Your resume did not match this job. Score: {link.score:.2f}. "
            "Consider adding skills or experience related to the job description."
        )

    # Save to AIFeedback table
    ai_feedback = AIFeedback(
        resume_id=resume_id,
        feedback_text=feedback_text
    )
    self.db.add(ai_feedback)
    self.db.commit()
    self.db.refresh(ai_feedback)
    return ai_feedback

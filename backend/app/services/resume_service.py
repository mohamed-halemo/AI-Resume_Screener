from backend.app.models.resume import Resume
from backend.app.models.personal_info import PersonalInfo
from sqlalchemy.orm import Session
from backend.app.services.resume_parser_service import ResumeParser
from uuid import UUID
from typing import List
from fastapi import HTTPException, status
from backend.app.models.resume import Resume
from backend.app.schemas.resume import ResumeUpdate

class ResumeService:
    def __init__(self, db: Session):
        self.db = db

    def _save_personal_info(self, resume_id: UUID, personal_info_str: str) -> PersonalInfo:
        fields = {}
        for line in personal_info_str.split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                fields[key.strip().lower()] = value.strip()

        personal_info = PersonalInfo(
            resume_id=resume_id,
            name=fields.get("name", "-"),
            email=fields.get("email", "-"),
            phone=fields.get("phone", "-"),
            address=fields.get("address", "-"),
            linkedin=fields.get("linkedin", "-"),
            github=fields.get("github", "-"),
            website=fields.get("website", "-")
        )
        self.db.add(personal_info)
        return personal_info

    def process_and_save_resume(self, user_id: UUID, file_path: str, use_groq: bool = False) -> Resume:
        parser = ResumeParser(file_path=file_path)
        data = parser.extract_with_groq() if use_groq else parser.extract_resume_sections()

        if not data or not isinstance(data, dict):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to extract resume content.")

        personal_info_str = data.pop("personal_info", "")
        parsed_text = data.get("parsed_text")
        if not parsed_text or parsed_text.strip() == "":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Resume content is empty.")

        resume_data = {
            k: data.get(k, None) for k in data 
            if k in Resume.__table__.columns and k != "parsed_text"
        }

        resume = Resume(user_id=user_id, parsed_text=parsed_text, **resume_data)
        self.db.add(resume)
        self.db.flush()  # To get resume.id

        if personal_info_str:
            self._save_personal_info(resume_id=resume.id, personal_info_str=personal_info_str)

        self.db.commit()
        self.db.refresh(resume)
        return resume




class ResumeUserService:
    def __init__(self, db: Session):
        self.db = db

    def list_user_resumes(self, user_id: UUID) -> List[Resume]:
        return self.db.query(Resume).filter(Resume.user_id == user_id).all()

    def get_user_resume(self, user_id: UUID, resume_id: UUID) -> Resume:
        resume = self.db.query(Resume).filter(
            Resume.user_id == user_id,
            Resume.id == resume_id
        ).first()
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found for this user")
        return resume

    def update_user_resume(self, user_id: UUID, resume_id: UUID, data: ResumeUpdate) -> Resume:
        resume = self.get_user_resume(user_id, resume_id)

        update_data = data.model_dump(exclude_unset=True, exclude_none=True)
        for field, value in update_data.items():
            setattr(resume, field, value)

        self.db.commit()
        self.db.refresh(resume)
        return resume

    def delete_user_resume(self, user_id: UUID, resume_id: UUID):
        resume = self.get_user_resume(user_id, resume_id)
        if resume.resume_job_links:  # checks if resume is linked to any job
            return {
                "message": "Resume is linked to one or more jobs. Please unlink it before deletion."
            }

        self.db.delete(resume)
        self.db.commit()
        return {"message": "Resume deleted successfully"}




class ResumeAdminService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_resumes(self):
        return self.db.query(Resume).all()

    def get_resume(self, resume_id: UUID):
        resume = self.db.query(Resume).filter(Resume.id == resume_id).first()
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")
        return resume

    def delete_resume(self, resume_id: UUID):
        resume = self.get_resume(resume_id)

        if resume.resume_job_links:
            # Delete all links first
            for link in resume.resume_job_links:
                self.db.delete(link)
        self.db.delete(resume)
        self.db.commit()
        return {"message": "Resume deleted successfully"}




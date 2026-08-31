from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
import tempfile
import shutil
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.services.user_service import get_current_user,require_role
from backend.app.services.resume_service import ResumeService,ResumeUserService,ResumeAdminService
from backend.app.schemas.resume import ResumeResponse,ResumeUpdate
from backend.app.models.user import User
from uuid import UUID
from typing import List



router = APIRouter(prefix="/resumes", tags=["Resume"])


# Users Resumes Upload Endpoints

@router.post("/upload-local")
def upload_resume_local(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    # if file.content_type not in ["application/pdf"]:
    #     raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    if file.filename == "":
        raise HTTPException(status_code=400, detail="No file provided.")

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    service = ResumeService(db)
    resume = service.process_and_save_resume(user_id=user.id, file_path=tmp_path, use_groq=False)
    return {"message": "Resume parsed and saved (local)", "resume_id": resume.id}


@router.post("/upload-groq")
def upload_resume_groq(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    # if file.content_type not in ["application/pdf"]:
    #     raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    if file.filename == "":
        raise HTTPException(status_code=400, detail="No file provided.")

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    service = ResumeService(db)
    resume = service.process_and_save_resume(user_id=user.id, file_path=tmp_path, use_groq=True)
    return {"message": "Resume parsed and saved (Groq)", "resume_id": resume.id}


# Users Resumes Management Endpoints

@router.get("/me", response_model=List[ResumeResponse])
def list_my_resumes(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return ResumeUserService(db).list_user_resumes(user.id)


@router.get("/me/{resume_id}", response_model=ResumeResponse)
def get_my_resume_by_id(
    resume_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return ResumeUserService(db).get_user_resume(user.id, resume_id)


@router.patch("/me/{resume_id}", response_model=ResumeResponse)
def update_my_resume(
    resume_id: UUID,
    data: ResumeUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return ResumeUserService(db).update_user_resume(user.id, resume_id, data)


@router.delete("/me/{resume_id}")
def delete_my_resume(
    resume_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return ResumeUserService(db).delete_user_resume(user.id, resume_id)




# Admins Resumes Management Endpoints

@router.get("/", response_model=list[ResumeResponse])
def get_all_resumes(
    db: Session = Depends(get_db),
    user: User = Depends(require_role("Admin"))
):
    service = ResumeAdminService(db)
    return service.get_all_resumes()


@router.get("/{resume_id}", response_model=ResumeResponse)
def get_resume_by_id(
    resume_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("Admin"))
):
    service = ResumeAdminService(db)
    return service.get_resume(resume_id)


@router.delete("/{resume_id}")
def delete_resume_by_id(
    resume_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("Admin"))
):
    service = ResumeAdminService(db)
    return service.delete_resume(resume_id)



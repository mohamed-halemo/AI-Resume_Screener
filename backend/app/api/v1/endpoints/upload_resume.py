# # --- app/api/v1/endpoints/upload_resume.py ---
# from fastapi import APIRouter, Depends, status, UploadFile, File, HTTPException
# from sqlalchemy.orm import Session
# from backend.app.core.database import get_db
# from backend.app.schemas.resume import ResumeCreate, ResumeResponse
# from backend.app.services.resume_service import process_resume_upload

# router = APIRouter()

# @router.post("", response_model=ResumeResponse, status_code=status.HTTP_201_CREATED)
# def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
#     return process_resume_upload(file, db)

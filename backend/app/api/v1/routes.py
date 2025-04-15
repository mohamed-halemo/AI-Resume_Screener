from fastapi import APIRouter
from backend.app.api.v1.endpoints import user 
from backend.app.api.v1.endpoints import job_description

router = APIRouter()

# Include user routes
router.include_router(user.router, prefix="/register", tags=["Users"])

router.include_router(job_description.router, prefix="/job-description", tags=["Job Descriptions"])
# router.include_router(job_description.router, prefix="/upload-resume", tags=["Upload Resume"])

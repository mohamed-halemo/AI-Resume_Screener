from fastapi import APIRouter
from backend.app.api.v1.endpoints import user 
from backend.app.api.v1.endpoints import job_description

router = APIRouter()

# Include user routes
router.include_router(user.router, prefix="/users", tags=["Users"])
router.include_router(job_description.router, prefix="/job-descriptions", tags=["Job Descriptions"])

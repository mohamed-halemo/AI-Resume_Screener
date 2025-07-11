from fastapi import APIRouter
from backend.app.api.v1.endpoints import (user_route,
                                          job_description_route,
                                          auth_route, resume_route,
                                          resume_job_link_route)

router = APIRouter(prefix="/api/v1")

# Include user routes
router.include_router(user_route.router)
router.include_router(auth_route.router)
router.include_router(job_description_route.router)
router.include_router(resume_route.router)
router.include_router(resume_job_link_route.router)


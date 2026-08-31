from fastapi import APIRouter, Depends, status
from backend.app.schemas import user as user_schemas
from backend.app.core.database import SessionLocal
from sqlalchemy.orm import Session
from backend.app.services.user_service import require_role,get_user_profile
from backend.app.core.database import get_db

router = APIRouter(prefix="/users",tags=["User"])



# Profile endpoint for authenticated user with role checking
@router.get("/profile", response_model=user_schemas.UserDetails)
def get_profile(
    db: Session = Depends(get_db),
    user: user_schemas.UserDetails = Depends(require_role("Admin","applicant", "HR"))  # Only Admin and HR roles can access
):
    """
    This endpoint returns the profile of the authenticated user.
    It uses the `require_role` dependency to check if the user's role is allowed.
    """
    # Call the service layer with the current_user extracted from the token
    return get_user_profile(db=db, user=user)
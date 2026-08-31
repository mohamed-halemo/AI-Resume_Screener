from fastapi import APIRouter, Depends, status
from backend.app.schemas import user as user_schemas
from backend.app.core.database import SessionLocal
from sqlalchemy.orm import Session
from backend.app.services.user_service import create_user, login_user
from backend.app.core.database import get_db

router = APIRouter(prefix="/auth",tags=["Auth"])




# Register user endpoint
@router.post("/register", response_model=user_schemas.UserCreate, status_code=status.HTTP_201_CREATED)
def register_user(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    print("received request")
    # Call the service to create a user and return the response
    return create_user(db, user)

# Login endpoint
@router.post("/login", response_model=user_schemas.LoginResponse)
def login_user_endpoint(form_data: user_schemas.LoginRequest, db: Session = Depends(get_db)):
    # Call the service to login the user
    return login_user(db, email=form_data.email, password=form_data.password)


from fastapi import APIRouter, Depends
from backend.app.schemas import user as user_schemas
from backend.app.core.database import SessionLocal
from sqlalchemy.orm import Session
from backend.app.services.user_service import login_user

router = APIRouter()

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Login endpoint
@router.post("/login", response_model=user_schemas.LoginResponse)
def login_user_endpoint(form_data: user_schemas.UserBase, db: Session = Depends(get_db)):
    # Call the service to login the user
    return login_user(db, email=form_data.email, password=form_data.password)

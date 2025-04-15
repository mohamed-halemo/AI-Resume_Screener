from fastapi import APIRouter, Depends, status
from backend.app.schemas import user as user_schemas
from backend.app.core.database import SessionLocal
from sqlalchemy.orm import Session
from backend.app.services.user_service import create_user  

router = APIRouter()

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Register user endpoint
@router.post("/register", response_model=user_schemas.UserCreate, status_code=status.HTTP_201_CREATED)
def register_user(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    print("received request")
    # Call the service to create a user and return the response
    return create_user(db, user)

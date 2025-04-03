from fastapi import APIRouter, HTTPException,Depends
from app.schemas import user as user_schemas
from app.core.database import SessionLocal
from app.models.user import User
from sqlalchemy.orm import Session

router = APIRouter()

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Route to register a user
@router.post("/register", response_model=user_schemas.UserCreate)
def create_user(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.name == user.name).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_user = User(username=user.name, email=user.email,role=user.role,password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

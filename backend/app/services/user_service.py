from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from backend.app.models.user import User
from backend.app.schemas.user import UserCreate, UserResponse
from fastapi import HTTPException
import logging
from backend.app.core.security import hash_password # Function to hash passwords

# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def create_user(db: Session, user: UserCreate) -> UserResponse:
    try:
        # Check if the user already exists
        db_user = db.query(User).filter(User.email == user.email).first()
        if db_user:
            raise HTTPException(status_code=400, detail="User already registered")

        # Hash the password before storing
        hashed_password = hash_password(user.password)

        # Create a new user instance
        db_user = User(
            name=user.name, 
            email=user.email, 
            role=user.role, 
            password=hashed_password  # Store hashed password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        # Return validated response
        return UserResponse.model_validate(db_user)

    except IntegrityError:
        db.rollback()
        logger.error("Database integrity error occurred while creating user")
        raise HTTPException(status_code=500, detail="A database error occurred. Please try again.")

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error. Please try again.")

  

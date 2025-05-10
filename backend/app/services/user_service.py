from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from backend.app.models.user import User
from backend.app.schemas.user import UserCreate, UserResponse
from backend.app.utils.security import create_access_token
from fastapi import HTTPException,status
import logging
from backend.app.schemas.user import LoginResponse
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from backend.app.core.security import hash_password,verify_password # Function to hash passwords

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

  
# Password hash context

# Function to get user by email
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


# Service function to handle user login
def login_user(db: Session, email: str, password: str) -> LoginResponse:
    user = get_user_by_email(db, email=email)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    # Verify password
    if not verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    # Generate JWT token
    access_token = create_access_token(data={"sub": user.email})
    
    # Return the response model
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        id=user.id,
        name=user.name,
        email=user.email,
        role=user.role,
        created_at=user.created_at
    )
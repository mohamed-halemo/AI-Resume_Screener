from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from fastapi import HTTPException,status,Header
import logging
from sqlalchemy.orm import Session
from fastapi import Depends
from jose import JWTError, jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


from backend.app.models.user import User
from backend.app.schemas.user import UserCreate, UserResponse, LoginResponse, UserDetails
from backend.app.utils.auth_utils import create_access_token, SECRET_KEY, ALGORITHM
from backend.app.core.security import hash_password,verify_password 
from backend.app.core.database import get_db

security = HTTPBearer()

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

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
    )

    
    if not user:
        raise credentials_exception
    
    # Verify password
    if not verify_password(password, user.password):
        raise credentials_exception
    
    # Generate JWT token
    access_token = create_access_token(data={"sub": user.email, "role": user.role})
    
    # Return the response model
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        created_at=user.created_at
    )






def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    
    token = credentials.credentials  # This gives just the token part (no 'Bearer' prefix)

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
    )
    

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception

    return user



def require_role(*allowed_roles):
    def checker(user: User = Depends(get_current_user)):
        if user.role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Operation not permitted")
        return user
    return checker

def get_user_profile(db: Session= Depends(get_db), user: User=Depends(require_role)) -> UserDetails:
    """
    Fetches the profile of the current authenticated user based on `user` object.
    """
    # user is passed from the `get_current_user` dependency and already contains the authenticated user info
    if not user:
        raise Exception("User not found")

    # Map User model to UserBase schema
    return UserDetails(
        id=user.id,
        name=user.name,
        email=user.email,
        role=user.role
    )
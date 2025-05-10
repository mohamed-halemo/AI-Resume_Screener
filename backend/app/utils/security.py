from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Any, Dict
from backend.app.core.config import settings

# Secret key to encode JWT tokens
SECRET_KEY = settings.SECRET_KEY  
ALGORITHM = settings.ALGORITHM  
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES  # Default token expiry time (minutes)

def create_access_token(data: Dict[str, Any], expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

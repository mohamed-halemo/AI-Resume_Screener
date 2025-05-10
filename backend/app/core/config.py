 
from pydantic_settings  import BaseSettings

class Settings(BaseSettings):
    database_url: str

    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # You can add DB connection string, CORS settings, etc.

    class Config:
        env_file = ".env"  # Optional: Load variables from a .env file

settings = Settings()

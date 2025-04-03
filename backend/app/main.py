 
from fastapi import FastAPI
from backend.app.api.v1.routes import router as api_router

app = FastAPI(title="AI-Powered Resume Screener", version="1.0")


app.include_router(api_router, prefix="/api/v1")



@app.get("/")
def root():
    return {"message": "Welcome to the AI-Powered Resume Screener API"}

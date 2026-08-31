 
from fastapi import FastAPI

from backend.app.api.v1 import routes
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="AI-Powered Resume Screener", version="1.0")


app.include_router(routes.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to the AI-Powered Resume Screener API"}


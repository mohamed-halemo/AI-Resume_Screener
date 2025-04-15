 
from fastapi import FastAPI
from backend.app.api.v1.endpoints import  job_description,user

app = FastAPI(title="AI-Powered Resume Screener", version="1.0")

# # Include API routes
# app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(job_description.router)
app.include_router(user.router)

# app.include_router(resumes.router, prefix="/resumes", tags=["Resumes"])
# app.include_router(ranking.router, prefix="/ranking", tags=["Resume Ranking"])
# app.include_router(feedback.router, prefix="/feedback", tags=["AI Feedback"])
# app.include_router(rerank.router, prefix="/rerank", tags=["AI Reranking"])

@app.get("/")
def root():
    return {"message": "Welcome to the AI-Powered Resume Screener API"}

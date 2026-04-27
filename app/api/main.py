from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings

app = FastAPI(
    title="Founder Intelligence Engine",
    description="AI system to evaluate startups using ML + LLM intelligence",
    version="1.0.0"
)

# CORS (important if you add frontend later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def root():
    return {
        "message": "Founder Intelligence Engine is running 🚀"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }
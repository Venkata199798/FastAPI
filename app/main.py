# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.routers import api_router
from app.db.session import engine
from app.models.base import BaseModel

# Create database tables / డేటాబేస్ టేబుల్స్ సృష్టించండి
BaseModel.metadata.create_all(bind=engine)

# Create FastAPI app / FastAPI app సృష్టించండి
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Student Management System API / విద్యార్థి నిర్వహణ వ్యవస్థ API",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Add CORS middleware / CORS మిడిల్వేర్ జోడించండి
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router / API router చేర్చండి
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    """
    English: Root endpoint - API health check
    Telugu: రూట్ endpoint - API ఆరోగ్య తనిఖీ
    """
    return {
        "message": "Welcome to Student Management System API",
        "version": settings.VERSION,
        "docs": "/api/docs"
    }

@app.get("/health")
def health_check():
    """
    English: Health check endpoint
    Telugu: ఆరోగ్య తనిఖీ endpoint
    """
    return {"status": "healthy"}
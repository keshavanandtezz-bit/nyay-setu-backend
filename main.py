from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

from routes.citizen import router as citizen_router
from routes.legal import router as legal_router
from routes.ai import router as ai_router
from routes.case import router as case_router
from routes.courts import router as courts_router

app = FastAPI(
    title="Nyay Setu API",
    description="AI-Powered Law Enforcement & Justice Platform — India",
    version="2.0.0"
)

# CORS — allow specific origins only
ALLOWED_ORIGINS = [
    "https://nyay-setu-kohl.vercel.app",
    "https://nyay-setu.vercel.app",
    "https://nyay-setu-beta.vercel.app",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register all routers
app.include_router(citizen_router)
app.include_router(legal_router)
app.include_router(ai_router)
app.include_router(case_router)
app.include_router(courts_router)


@app.get("/")
def root():
    return {
        "status": "online",
        "message": "Nyay Setu API is running",
        "version": "2.0.0",
        "endpoints": {
            "citizen": "/citizen",
            "legal": "/legal",
            "ai": "/ai",
            "case": "/case",
            "courts": "/courts",
            "docs": "/docs",
            "health": "/health"
        }
    }


@app.get("/health")
def health_check():
    try:
        from db.mongo_client import db
        db.command("ping")
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    return {"status": "healthy", "api": "Nyay Setu", "database": db_status}
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

from routes.citizen import router as citizen_router
from routes.legal import router as legal_router
from routes.ai import router as ai_router

app = FastAPI(
    title="Nyay Setu API",
    description="AI-Powered Law Enforcement & Justice Platform — India",
    version="1.0.0"
)

# CORS — allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "nyay-setu-kohl.vercel.app",
        "https://nyay-setu-keshavanandtezz-bit.vercel.app",
        os.getenv("FRONTEND_URL", "http://localhost:3000"),
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register all routers
app.include_router(citizen_router)
app.include_router(legal_router)
app.include_router(ai_router)


@app.get("/")
def root():
    return {
        "status": "online",
        "message": "Nyay Setu API is running",
        "version": "1.0.0",
        "endpoints": {
            "citizen": "/citizen",
            "legal": "/legal",
            "ai": "/ai",
            "docs": "/docs"
        }
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "api": "Nyay Setu"}
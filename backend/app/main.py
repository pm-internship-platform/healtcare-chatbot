# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import os
from pathlib import Path
from .api import chat, health_info, users, gamification
from .utils.logger import setup_logging, log_info
from .utils.config import get_settings
from .db.mongo import connect_to_mongo, close_mongo_connection

# Setup logging
setup_logging()

# Get application settings
settings = get_settings()

# Get the base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

# Create FastAPI application
app = FastAPI(
    title="Odisha AI Health Chatbot API",
    description="API for AI-Driven Public Health Chatbot for Government of Odisha",
    version="1.0.0"
)

# Configure CORS - allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix="/api")
app.include_router(health_info.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(gamification.router, prefix="/api")

# Serve static files (frontend) - only if the directory exists
if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
    log_info(f"Serving frontend from: {FRONTEND_DIR}")
else:
    log_info(f"Frontend directory not found: {FRONTEND_DIR}")

# Database connection events
@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()
    log_info("Application started")

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()
    log_info("Application shutdown")

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}
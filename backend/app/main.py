from fastapi import FastAPI

# Import settings instance
from app.config import settings

# Import routers
from backend.routes import chat, health, survey, auth

# Import middleware
from backend.core.middleware import RequestIDMiddleware, TimingMiddleware

# Import database
from backend.services.db_service import db

# Create FastAPI instance
app = FastAPI(title="AI Health Chatbot", version="1.0")

# Add middlewares
app.add_middleware(RequestIDMiddleware)
app.add_middleware(TimingMiddleware)

# Database events
@app.on_event("startup")
async def startup_db():
    """Connect to MongoDB on startup."""
    await db.connect()

@app.on_event("shutdown")
async def shutdown_db():
    """Disconnect from MongoDB on shutdown."""
    await db.disconnect()

# Include routes
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(health.router, prefix="/api/health", tags=["health"])
app.include_router(survey.router, prefix="/api/survey", tags=["survey"])

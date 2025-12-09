"""
Test Case Management (TCM) - Main Application Entry Point

This module initializes the FastAPI application and includes all routes.
"""

import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from tcm.config import settings
from tcm.routes import tags, testcases, projects, auth

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

app = FastAPI(
    title="Test Case Management",
    description="Web application for test case creation and tracking",
    version="0.1.0",
)

# Mount static files
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Include routers
app.include_router(auth.router)  # Authentication routes (no prefix for /login)
app.include_router(tags.router, prefix="/api")
app.include_router(testcases.router, prefix="/api")
app.include_router(projects.router, prefix="/api")


@app.get("/")
async def root():
    """Root endpoint - health check."""
    return {
        "message": "Test Case Management API",
        "version": "0.1.0",
        "status": "running",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "tcm.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )

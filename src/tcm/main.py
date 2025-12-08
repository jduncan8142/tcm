"""
Test Case Management (TCM) - Main Application Entry Point

This module initializes the FastAPI application and includes all routes.
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from tcm.config import settings

app = FastAPI(
    title="Test Case Management",
    description="Web application for test case creation and tracking",
    version="0.1.0",
)


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

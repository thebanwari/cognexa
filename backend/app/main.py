from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from typing import Dict, Any
import logging
import os

from app.models.response_models import HealthResponse
from app.config import PDF_OUTPUT_DIR

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="CourseCraft-AI",
    description="AI-powered course generation and learning platform",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for PDF and mindmap serving
mindmap_dir = "static/mindmaps"
pdf_dir = "app/static/pdf"

# Create mindmap directory if it doesn't exist
os.makedirs(mindmap_dir, exist_ok=True)

# Mount mindmap static files
app.mount("/static/mindmaps", StaticFiles(directory=mindmap_dir), name="mindmaps")
logger.info(f"Mounted mindmap static files at /static/mindmaps serving {mindmap_dir}")

# Mount PDF static files
if os.path.exists(PDF_OUTPUT_DIR):
    app.mount("/static/pdf", StaticFiles(directory=PDF_OUTPUT_DIR), name="pdf_files")
    logger.info(f"Mounted PDF static files at /static/pdf serving {PDF_OUTPUT_DIR}")
else:
    logger.warning(f"PDF output directory {PDF_OUTPUT_DIR} does not exist, creating...")
    os.makedirs(PDF_OUTPUT_DIR, exist_ok=True)
    app.mount("/static/pdf", StaticFiles(directory=PDF_OUTPUT_DIR), name="pdf_files")


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "success": False
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "Internal server error",
            "success": False
        }
    )


@app.get("/", response_model=Dict[str, Any])
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to CourseCraft-AI API",
        "version": "1.0.0",
        "documentation": "/docs",
        "endpoints": {
            "generate_course": "POST /generate-course",
            "generate_pdf": "POST /generate-pdf",
            "ask_question": "POST /ask",
            "health": "GET /health"
        }
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp="2024-01-01T00:00:00Z"  # Will be overridden by model
    )


@app.get("/api/v1/status")
async def api_status():
    """API status endpoint"""
    return {
        "status": "active",
        "version": "1.0.0",
        "features": {
            "course_generation": True,
            "pdf_generation": True,
            "rag_qa": True,
            "session_management": True
        },
        "uptime": "running"
    }


# Include routers
from app.routes.course_routes import router as course_router
from app.routes.mindmap_routes import router as mindmap_router
from app.routes.rag_routes import router as rag_router


app.include_router(course_router, prefix="/api/v1", tags=["Course Generation"])
app.include_router(mindmap_router, prefix="/api/v1", tags=["Mindmap Generation"])
app.include_router(rag_router, prefix="/api/v1", tags=["RAG Q&A"])

# Include other routers as they are implemented
from app.routes.assignment_routes import router as assignment_router
app.include_router(assignment_router, prefix="/api/v1", tags=["Assignment Generation"])

from app.routes.flashcard_routes import router as flashcard_router
app.include_router(flashcard_router, prefix="/api/v1", tags=["Flashcard Generation"])


# Custom OpenAPI schema with proper tags
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    from fastapi.openapi.utils import get_openapi

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
        tags=[
            {"name": "Course Generation", "description": "Course creation and management endpoints"},
            {"name": "Assignment Generation", "description": "Assignment generation and retrieval"},
            {"name": "Flashcard Generation", "description": "Flashcard generation and retrieval"},
            {"name": "Mindmap Generation", "description": "Mindmap generation and visualization"},
            {"name": "RAG Q&A", "description": "Retrieval-Augmented Generation question answering"},
        ]
    )

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# from app.routes.studyplan_routes import router as studyplan_router
# app.include_router(studyplan_router, prefix="/api/v1", tags=["Study Plan Generation"])

# from app.routes.auth_routes import router as auth_router
# app.include_router(auth_router, prefix="/api/v1", tags=["Authentication"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
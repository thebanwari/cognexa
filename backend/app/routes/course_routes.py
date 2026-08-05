from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Dict, Any
import logging
import os

from app.models.request_models import GenerateCourseRequest, GeneratePDFRequest
from app.models.response_models import CourseResponse, PDFResponse
from app.services.llm_service import mock_llm_course_generator
from app.services.pdf_service import generate_course_pdf
from app.utils.session_store import session_store
from app.utils.file_manager import ensure_directory_exists
from app.config import PDF_OUTPUT_DIR

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/generate-course", response_model=CourseResponse)
async def generate_course(request: GenerateCourseRequest):
    """
    Generate a complete course structure based on topic, duration, difficulty, and language.

    Args:
        request: Course generation parameters

    Returns:
        CourseResponse with session ID and course data
    """
    try:
        logger.info(f"Generating course for topic: {request.topic}")

        # Validate input parameters
        if request.duration < 1 or request.duration > 24:
            raise HTTPException(
                status_code=400,
                detail="Duration must be between 1 and 24 weeks"
            )

        if request.difficulty not in ["beginner", "intermediate", "advanced"]:
            raise HTTPException(
                status_code=400,
                detail="Difficulty must be one of: beginner, intermediate, advanced"
            )

        if request.language not in ["english", "hindi"]:
            raise HTTPException(
                status_code=400,
                detail="Language must be one of: english, hindi"
            )

        # Generate course using mock LLM
        course_data = mock_llm_course_generator(
            topic=request.topic,
            duration=request.duration,
            difficulty=request.difficulty,
            language=request.language
        )

        if not course_data:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate course content"
            )

        # Store course data in session
        session_data = {
            "course": course_data,
            "topic": request.topic,
            "duration": request.duration,
            "difficulty": request.difficulty,
            "language": request.language,
            "created_at": course_data.get("created_at", "N/A")
        }

        session_id = session_store.create_session(session_data)

        logger.info(f"Course generated successfully with session ID: {session_id}")

        return CourseResponse(
            session_id=session_id,
            course=course_data,
            message="Course generated successfully",
            success=True
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating course: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.post("/generate-pdf", response_model=PDFResponse)
async def generate_pdf(request: GeneratePDFRequest):
    """
    Generate a PDF version of the course.

    Args:
        request: PDF generation request with session ID

    Returns:    
        PDFResponse with PDF URL
    """
    try:
        logger.info(f"Generating PDF for session: {request.session_id}")

        # Check if session exists
        session_data = session_store.get_session(request.session_id)
        if not session_data:
            raise HTTPException(
                status_code=404,
                detail="Session not found or expired"
            )

        # Get course data
        course_data = session_data.get("course")
        if not course_data:
            raise HTTPException(
                status_code=400,
                detail="No course data found in session"
            )

        # Ensure PDF output directory exists
        if not ensure_directory_exists(PDF_OUTPUT_DIR):
            raise HTTPException(
                status_code=500,
                detail="Failed to create PDF output directory"
            )

        # Generate filename
        course_title = course_data.get("title", "course")
        sanitized_title = "".join(c for c in course_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        filename = f"{sanitized_title.replace(' ', '_')}_{request.session_id}.pdf"
        pdf_path = os.path.join(PDF_OUTPUT_DIR, filename)

        # Generate PDF
        success = generate_course_pdf(course_data, pdf_path)
        if not success:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate PDF"
            )

        # Generate PDF URL (relative path for now)
        pdf_url = f"/static/pdf/{filename}"

        logger.info(f"PDF generated successfully: {pdf_path}")

        return PDFResponse(
            session_id=request.session_id,
            pdf_url=pdf_url,
            message="PDF generated successfully",
            success=True
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating PDF: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/session/{session_id}")
async def get_session_info(session_id: str):
    """
    Get information about a session.

    Args:
        session_id: Session ID

    Returns:
        Session information
    """
    try:
        session_data = session_store.get_session_info(session_id)
        if not session_data:
            raise HTTPException(
                status_code=404,
                detail="Session not found or expired"
            )

        return {
            "session_id": session_id,
            "exists": True,
            "info": session_data
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting session info: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/sessions")
async def list_sessions():
    """
    List all active sessions (for debugging).

    Returns:
        Dictionary of active sessions
    """
    try:
        sessions = session_store.list_sessions()
        return {
            "total_sessions": len(sessions),
            "sessions": sessions
        }

    except Exception as e:
        logger.error(f"Error listing sessions: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.delete("/session/{session_id}")
async def delete_session(session_id: str):
    """
    Delete a session (for debugging).

    Args:
        session_id: Session ID

    Returns:
        Deletion status
    """
    try:
        success = session_store.delete_session(session_id)
        if not success:
            raise HTTPException(
                status_code=404,
                detail="Session not found"
            )

        # Also clean up RAG index if it exists
        try:
            from app.services.rag_service import cleanup_rag_session
            cleanup_rag_session(session_id)
        except Exception as e:
            logger.warning(f"Error cleaning up RAG session: {e}")

        return {
            "message": "Session deleted successfully",
            "success": True
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting session: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/course/{session_id}")
async def get_course_data(session_id: str):
    """
    Get the course data for a session.

    Args:
        session_id: Session ID

    Returns:
        Course data
    """
    try:
        session_data = session_store.get_session(session_id)
        if not session_data:
            raise HTTPException(
                status_code=404,
                detail="Session not found or expired"
            )

        course_data = session_data.get("course")
        if not course_data:
            raise HTTPException(
                status_code=404,
                detail="No course data found in session"
            )

        return course_data

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting course data: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
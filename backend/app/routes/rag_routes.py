from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
import logging

from app.models.request_models import AskRequest
from app.models.response_models import AskResponse
from app.services.rag_service import create_rag_index, query_rag_index, get_rag_service

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest):
    """
    Ask a question about the course using RAG system.

    Args:
        request: Question and session ID

    Returns:
        Answer and source information
    """
    try:
        logger.info(f"Processing question for session: {request.session_id}")

        # Check if session exists
        from app.utils.session_store import session_store
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
                status_code=404,
                detail="No course data found in session"
            )

        # Initialize RAG service if not already done
        rag_service = get_rag_service(request.session_id)

        # Check if RAG index exists, if not create it
        if not rag_service.chunks or not rag_service.embeddings:
            logger.info(f"Creating RAG index for session: {request.session_id}")
            success = create_rag_index(request.session_id, course_data)
            if not success:
                raise HTTPException(
                    status_code=500,
                    detail="Failed to initialize RAG system"
                )

        # Query the RAG system
        answer, source_chunks = query_rag_index(
            session_id=request.session_id,
            question=request.query,
            top_k=3
        )

        logger.info(f"Generated answer for question: {request.query[:50]}...")

        return AskResponse(
            session_id=request.session_id,
            question=request.query,
            answer=answer,
            sources=source_chunks,
            success=True
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing question: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/rag-info/{session_id}")
async def get_rag_info(session_id: str):
    """
    Get RAG system information for a session.

    Args:
        session_id: Session ID

    Returns:
        RAG system information
    """
    try:
        # Check if session exists
        from app.utils.session_store import session_store
        session_data = session_store.get_session(session_id)
        if not session_data:
            raise HTTPException(
                status_code=404,
                detail="Session not found or expired"
            )

        # Get RAG service info
        rag_service = get_rag_service(session_id)
        rag_info = rag_service.get_session_info()

        return {
            "session_id": session_id,
            "rag_info": rag_info,
            "course_title": session_data.get("course", {}).get("title", "N/A")
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting RAG info: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.post("/rag-simulate/{session_id}")
async def simulate_rag_query(session_id: str, question: str):
    """
    Simulate RAG query to get relevant chunks without generating answer (for debugging).

    Args:
        session_id: Session ID
        question: Test question

    Returns:
        Relevant chunks with similarity scores
    """
    try:
        # Check if session exists
        from app.utils.session_store import session_store
        session_data = session_store.get_session(session_id)
        if not session_data:
            raise HTTPException(
                status_code=404,
                detail="Session not found or expired"
            )

        # Get course data
        course_data = session_data.get("course")
        if not course_data:
            raise HTTPException(
                status_code=404,
                detail="No course data found in session"
            )

        # Initialize RAG service
        rag_service = get_rag_service(session_id)

        # Check if RAG index exists, if not create it
        if not rag_service.chunks or not rag_service.embeddings:
            success = create_rag_index(session_id, course_data)
            if not success:
                raise HTTPException(
                    status_code=500,
                    detail="Failed to initialize RAG system"
                )

        # Get relevant chunks
        relevant_chunks = rag_service.get_relevant_chunks(question, top_k=3)

        return {
            "session_id": session_id,
            "question": question,
            "relevant_chunks": relevant_chunks,
            "total_chunks": len(rag_service.chunks)
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error simulating RAG query: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/rag-chunks/{session_id}")
async def get_chunk_info(session_id: str):
    """
    Get information about chunks for a session (for debugging).

    Args:
        session_id: Session ID

    Returns:
        Chunk information
    """
    try:
        # Check if session exists
        from app.utils.session_store import session_store
        session_data = session_store.get_session(session_id)
        if not session_data:
            raise HTTPException(
                status_code=404,
                detail="Session not found or expired"
            )

        # Get RAG service
        rag_service = get_rag_service(session_id)

        # Check if RAG index exists
        if not rag_service.chunks or not rag_service.embeddings:
            raise HTTPException(
                status_code=404,
                detail="No RAG index found for this session"
            )

        # Return chunk information
        chunk_info = []
        for i, chunk in enumerate(rag_service.chunks):
            chunk_info.append({
                "chunk_index": i,
                "content_preview": chunk[:200] + "..." if len(chunk) > 200 else chunk,
                "content_length": len(chunk),
                "has_embedding": i < len(rag_service.embeddings)
            })

        return {
            "session_id": session_id,
            "total_chunks": len(rag_service.chunks),
            "total_embeddings": len(rag_service.embeddings),
            "chunks": chunk_info
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting chunk info: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
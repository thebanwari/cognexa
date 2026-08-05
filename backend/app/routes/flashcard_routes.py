from fastapi import APIRouter, HTTPException
from app.models.request_models import FlashcardRequest
from app.models.response_models import FlashcardResponse
from app.services.flashcard_service import generate_flashcards

router = APIRouter()


@router.post("/flashcards/generate", response_model=FlashcardResponse)
async def generate_flashcards_endpoint(request: FlashcardRequest):
    """
    Generate flashcards for a course or specific topic.

    Args:
        request: FlashcardRequest with session_id, optional topic and difficulty

    Returns:
        FlashcardResponse with enriched flashcards
    """
    try:
        result = generate_flashcards(
            session_id=request.session_id,
            topic=request.topic,
            difficulty=request.difficulty,
        )

        if not result["success"]:
            raise HTTPException(
                status_code=400,
                detail=result.get("message", "Failed to generate flashcards")
            )

        return FlashcardResponse(
            success=True,
            flashcards=result["flashcards"],
            topic=result.get("topic"),
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/flashcards/{session_id}", response_model=FlashcardResponse)
async def get_flashcards_endpoint(session_id: str):
    """
    Get previously generated flashcards for a session.
    """
    try:
        result = generate_flashcards(session_id)

        if not result["success"]:
            raise HTTPException(
                status_code=404,
                detail=result.get("message", "No flashcards found for this session")
            )

        return FlashcardResponse(
            success=True,
            flashcards=result["flashcards"],
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
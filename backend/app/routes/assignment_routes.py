from fastapi import APIRouter, HTTPException
from app.models.request_models import AssignmentRequest
from app.models.response_models import AssignmentResponse

from app.services.assignment_service import generate_assignments

router = APIRouter()


@router.post("/assignments/generate", response_model=AssignmentResponse)
async def generate_assignments_endpoint(request: AssignmentRequest):
    """
    Generate assignments for a course.

    Args:
        request: Assignment request containing session_id

    Returns:
        AssignmentResponse with success status and assignments
    """
    try:
        result = generate_assignments(request.session_id)

        if not result["success"]:
            raise HTTPException(
                status_code=400,
                detail=result.get("message", "Failed to generate assignments")
            )

        return AssignmentResponse(
            success=True,
            assignments=result["assignments"]
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/assignments/{session_id}", response_model=AssignmentResponse)
async def get_assignments_endpoint(session_id: str):
    """
    Get previously generated assignments for a session.

    Args:
        session_id: Session identifier

    Returns:
        AssignmentResponse with success status and assignments
    """
    try:
        result = generate_assignments(session_id)

        if not result["success"]:
            raise HTTPException(
                status_code=404,
                detail=result.get("message", "No assignments found for this session")
            )

        return AssignmentResponse(
            success=True,
            assignments=result["assignments"]
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
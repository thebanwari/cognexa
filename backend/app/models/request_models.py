from pydantic import BaseModel, Field
from typing import List, Optional


class GenerateCourseRequest(BaseModel):
    """Request model for course generation"""
    topic: str = Field(..., description="The topic for which to generate a course")
    duration: int = Field(default=4, ge=1, le=24, description="Duration in weeks (1-24)")
    difficulty: str = Field(default="beginner", description="Difficulty level: beginner, intermediate, advanced")
    language: str = Field(default="english", description="Language: english, hindi")

    class Config:
        schema_extra = {
            "example": {
                "topic": "Python Programming",
                "duration": 6,
                "difficulty": "beginner",
                "language": "english"
            }
        }


class AskRequest(BaseModel):
    """Request model for RAG Q&A"""
    session_id: str = Field(..., description="Session ID from course generation")
    query: str = Field(..., description="User's question about the course")

    class Config:
        schema_extra = {
            "example": {
                "session_id": "session_12345",
                "query": "What are the main concepts covered in week 3?"
            }
        }


class GeneratePDFRequest(BaseModel):
    """Request model for PDF generation"""
    session_id: str = Field(..., description="Session ID from course generation")

    class Config:
        schema_extra = {
            "example": {
                "session_id": "session_12345"
            }
        }


class AssignmentRequest(BaseModel):
    """Request model for assignment generation"""
    session_id: str = Field(..., description="Session ID from course generation")

    class Config:
        schema_extra = {
            "example": {
                "session_id": "session_12345"
            }
        }


class FlashcardRequest(BaseModel):
    """Request model for flashcard generation"""
    session_id: str = Field(..., description="Session ID from course generation")
    topic: Optional[str] = Field(default=None, description="Specific topic/day title to generate flashcards for")
    difficulty: Optional[str] = Field(default="beginner", description="Difficulty level: beginner, intermediate, advanced")

    class Config:
        schema_extra = {
            "example": {
                "session_id": "session_12345",
                "topic": "Python Strings",
                "difficulty": "beginner"
            }
        }
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class CourseResponse(BaseModel):
    """Response model for course generation"""
    session_id: str
    course: dict  # Course model serialized as dict
    message: str
    success: bool


class AskResponse(BaseModel):
    """Response model for RAG Q&A"""
    session_id: str
    question: str
    answer: str
    sources: List[str]  # List of source chunks used
    success: bool


class PDFResponse(BaseModel):
    """Response model for PDF generation"""
    session_id: str
    pdf_url: str
    message: str
    success: bool


class AssignmentResponse(BaseModel):
    """Response model for assignment generation"""
    success: bool
    assignments: List[dict]  # List of assignment dictionaries
    message: Optional[str] = None


class FlashcardItem(BaseModel):
    """Single enriched flashcard"""
    question: str
    answer: str
    hint: Optional[str] = None
    difficulty: str = "easy"
    tags: List[str] = []


class FlashcardResponse(BaseModel):
    """Response model for flashcard generation"""
    success: bool
    flashcards: List[FlashcardItem]
    topic: Optional[str] = None
    message: Optional[str] = None


class HealthResponse(BaseModel):
    """Response model for health check"""
    status: str = "healthy"
    timestamp: datetime
    version: str = "1.0.0"
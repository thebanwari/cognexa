from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class Day(BaseModel):
    """Represents a single day's learning content"""
    day_number: int
    title: str
    objectives: List[str]
    content: str
    activities: List[str]
    resources: Optional[List[str]] = Field(default_factory=list)


class Week(BaseModel):
    """Represents a week's learning content"""
    week_number: int
    title: str
    objectives: List[str]
    days: List[Day]


class Assignment(BaseModel):
    """Represents an assignment or quiz"""
    title: str
    type: str  # "MCQ", "coding", "theory"
    difficulty: str  # "beginner", "intermediate", "advanced"
    questions: List[str]
    solutions: Optional[List[str]] = Field(default_factory=list)


class Flashcard(BaseModel):
    """Represents a flashcard for revision"""
    front: str
    back: str
    category: str


class Course(BaseModel):
    """Complete course structure"""
    course_id: str
    title: str
    description: str
    difficulty: str  # "beginner", "intermediate", "advanced"
    language: str  # "english", "hindi"
    duration_weeks: int
    learning_objectives: List[str]
    prerequisites: List[str]
    weeks: List[Week]
    assignments: List[Assignment]
    flashcards: List[Flashcard]
    created_at: datetime
    total_days: int

    def get_total_content(self) -> str:
        """Extract all text content for RAG processing"""
        content_parts = [
            f"Course: {self.title}",
            f"Description: {self.description}",
            f"Learning Objectives: {', '.join(self.learning_objectives)}",
            f"Prerequisites: {', '.join(self.prerequisites)}"
        ]

        for week in self.weeks:
            content_parts.append(f"\nWeek {week.week_number}: {week.title}")
            content_parts.extend([f"- Objective: {obj}" for obj in week.objectives])

            for day in week.days:
                content_parts.append(f"\nDay {day.day_number}: {day.title}")
                content_parts.extend([f"- Objective: {obj}" for obj in day.objectives])
                content_parts.append(f"Content: {day.content}")
                content_parts.extend([f"- Activity: {act}" for act in day.activities])

        return "\n".join(content_parts)
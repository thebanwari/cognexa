import json
import hashlib
from datetime import datetime
from typing import Dict, Any, List, Optional
from app.models.course_models import Course, Week, Day, Assignment, Flashcard
from app.utils.text_cleaner import clean_text
from app.services.llm_service import mock_llm_rag_answer
from app.utils.session_store import session_store


def generate_assignments(session_id: str) -> Dict[str, Any]:
    """
    Generate assignments for a course using session data and LLM.

    Args:
        session_id: Session identifier

    Returns:
        Dictionary with success status and assignments
    """
    try:
        # Get session data
        session_data = session_store.get_session(session_id)
        if not session_data:
            return {
                "success": False,
                "message": "Session not found or expired"
            }

        # Extract course content from session
        course_content = session_data.get("course", "")
        if not course_content:
            return {
                "success": False,
                "message": "No course content available for assignment generation"
            }

        # Generate assignments using LLM
        assignments = _create_assignments_from_content(course_content, session_id)

        return {
            "success": True,
            "assignments": assignments,
            "generated_at": datetime.now().isoformat()
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Error generating assignments: {str(e)}"
        }


def _create_assignments_from_content(course_content: str, session_id: str) -> List[Dict[str, str]]:
    """
    Create assignments from course content using LLM.

    Args:
        course_content: Course content text
        session_id: Session identifier

    Returns:
        List of assignment dictionaries
    """
    # Mock assignment generation based on content
    # In a real implementation, this would use OpenAI API

    # Extract key topics from content (mock implementation)
    topics = _extract_topics_from_content(course_content)

    assignments = []

    # Generate MCQ assignments
    for i, topic in enumerate(topics[:3]):  # Generate 3 MCQ assignments
        assignment = {
            "type": "MCQ",
            "question": f"What is the key concept of {topic}?",
            "answer": f"The key concept of {topic} is fundamental to understanding the broader {topic} principles."
        }
        assignments.append(assignment)

    # Generate short answer assignments
    for i, topic in enumerate(topics[:2]):  # Generate 2 short answer assignments
        assignment = {
            "type": "SHORT",
            "question": f"Explain the importance of {topic} in practical applications.",
            "answer": f"{topic} is crucial because it forms the foundation for advanced concepts and real-world implementations."
        }
        assignments.append(assignment)

    # Generate long answer assignment
    if topics:
        assignment = {
            "type": "LONG",
            "question": f"Discuss the comprehensive role of {topics[0]} in the context of the entire course.",
            "answer": f"{topics[0]} serves as a cornerstone concept that connects multiple aspects of the course. "
                     f"It provides the theoretical foundation and practical framework for understanding subsequent topics. "
                     f"Mastery of {topics[0]} enables students to approach complex problems with confidence."
        }
        assignments.append(assignment)

    return assignments


def _extract_topics_from_content(content: str) -> List[str]:
    """
    Extract key topics from course content.

    Args:
        content: Course content text

    Returns:
        List of topics
    """
    # Mock topic extraction
    # In a real implementation, this would use NLP techniques

    content_lower = content.lower()

    if "python" in content_lower:
        return [
            "Python Fundamentals",
            "Data Structures",
            "Control Flow",
            "Functions",
            "Object-Oriented Programming"
        ]
    elif "web" in content_lower:
        return [
            "HTML Basics",
            "CSS Styling",
            "JavaScript Fundamentals",
            "DOM Manipulation",
            "Responsive Design"
        ]
    elif "machine learning" in content_lower:
        return [
            "Statistics Foundation",
            "Data Preprocessing",
            "Supervised Learning",
            "Model Evaluation",
            "Deep Learning Basics"
        ]
    else:
        # Default topics for unknown content
        return [
            "Core Concepts",
            "Practical Applications",
            "Theoretical Foundation",
            "Real-world Examples",
            "Advanced Topics"
        ]
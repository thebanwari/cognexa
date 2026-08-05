import os
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import logging

from app.utils.chunking import chunk_course_content
from app.utils.embeddings import get_text_embedding, cosine_similarity
from app.services.llm_service import mock_llm_rag_answer
from app.utils.file_manager import save_file, load_file

logger = logging.getLogger(__name__)


class RAGService:
    """RAG (Retrieval Augmented Generation) service for course Q&A"""

    def __init__(self, session_id: str):
        """
        Initialize RAG service for a session.

        Args:
            session_id: Session ID
        """
        self.session_id = session_id
        self.course_data: Optional[Dict[str, Any]] = None
        self.chunks: List[str] = []
        self.embeddings: List[List[float]] = []
        self.index_file = f"rag_index_{session_id}.json"

    def load_course_data(self, course_data: Dict[str, Any]) -> bool:
        """
        Load course data and prepare for RAG.

        Args:
            course_data: Course data

        Returns:
            True if successful
        """
        try:
            self.course_data = course_data

            # Extract text content from course
            if not self._extract_course_text():
                logger.error("Failed to extract course text")
                return False

            # Create chunks
            self.chunks = chunk_course_content(self._extract_course_text())
            logger.info(f"Created {len(self.chunks)} chunks from course content")

            # Generate embeddings
            self.embeddings = [get_text_embedding(chunk) for chunk in self.chunks]
            logger.info(f"Generated embeddings for {len(self.embeddings)} chunks")

            # Save index
            self._save_index()

            return True

        except Exception as e:
            logger.error(f"Error loading course data: {e}")
            return False

    def _extract_course_text(self) -> str:
        """Extract all text content from course data"""
        if not self.course_data:
            return ""

        # Use the get_total_content method if available
        try:
            # Convert dict to Course object temporarily to use the method
            from app.models.course_models import Course
            course = Course(**self.course_data)
            return course.get_total_content()
        except:
            # Fallback: manual extraction
            content_parts = [
                f"Course: {self.course_data.get('title', '')}",
                f"Description: {self.course_data.get('description', '')}",
                f"Learning Objectives: {', '.join(self.course_data.get('learning_objectives', []))}",
                f"Prerequisites: {', '.join(self.course_data.get('prerequisites', []))}"
            ]

            for week in self.course_data.get('weeks', []):
                week_content = f"\nWeek {week.get('week_number', 0)}: {week.get('title', '')}"
                week_content += f"\nObjectives: {', '.join(week.get('objectives', []))}"

                for day in week.get('days', []):
                    day_content = f"\nDay {day.get('day_number', 0)}: {day.get('title', '')}"
                    day_content += f"\nObjectives: {', '.join(day.get('objectives', []))}"
                    day_content += f"\nContent: {day.get('content', '')}"
                    day_content += f"\nActivities: {', '.join(day.get('activities', []))}"
                    week_content += day_content

                content_parts.append(week_content)

            return "\n".join(content_parts)

    def _save_index(self) -> bool:
        """Save RAG index to file"""
        try:
            index_data = {
                "session_id": self.session_id,
                "chunks": self.chunks,
                "embeddings": self.embeddings,
                "created_at": datetime.now().isoformat()
            }

            # Save to temp directory
            temp_dir = "temp"
            os.makedirs(temp_dir, exist_ok=True)
            index_path = os.path.join(temp_dir, self.index_file)

            import json
            with open(index_path, 'w') as f:
                json.dump(index_data, f, indent=2)

            logger.info(f"Saved RAG index to {index_path}")
            return True

        except Exception as e:
            logger.error(f"Error saving RAG index: {e}")
            return False

    def _load_index(self) -> bool:
        """Load RAG index from file"""
        try:
            temp_dir = "temp"
            index_path = os.path.join(temp_dir, self.index_file)

            if not os.path.exists(index_path):
                logger.warning(f"RAG index not found: {index_path}")
                return False

            import json
            with open(index_path, 'r') as f:
                index_data = json.load(f)

            self.chunks = index_data.get("chunks", [])
            self.embeddings = index_data.get("embeddings", [])
            logger.info(f"Loaded RAG index with {len(self.chunks)} chunks")
            return True

        except Exception as e:
            logger.error(f"Error loading RAG index: {e}")
            return False

    def query(self, question: str, top_k: int = 3) -> Tuple[str, List[str]]:
        """
        Query the RAG system.

        Args:
            question: User's question
            top_k: Number of top chunks to retrieve

        Returns:
            Tuple of (answer, source_chunks)
        """
        try:
            # Load index if not already loaded
            if not self.chunks or not self.embeddings:
                if not self._load_index():
                    return "Course data not available for Q&A.", []

            # Generate query embedding
            query_embedding = get_text_embedding(question)

            # Compute similarities
            similarities = []
            for i, chunk_embedding in enumerate(self.embeddings):
                similarity = cosine_similarity(query_embedding, chunk_embedding)
                similarities.append((i, similarity))

            # Sort by similarity and get top k
            similarities.sort(key=lambda x: x[1], reverse=True)
            top_indices = [idx for idx, _ in similarities[:top_k]]

            # Get context from top chunks
            context_chunks = [self.chunks[i] for i in top_indices]

            # Construct context for LLM
            context = "\n\n".join(context_chunks)

            # Generate answer using mock LLM
            course_title = self.course_data.get('title', 'Course') if self.course_data else 'Course'
            answer = mock_llm_rag_answer(question, context, course_title)

            logger.info(f"Generated RAG answer for question: {question[:50]}...")
            return answer, context_chunks

        except Exception as e:
            logger.error(f"Error in RAG query: {e}")
            return f"Sorry, I encountered an error while processing your question: {str(e)}", []

    def get_relevant_chunks(self, question: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Get relevant chunks without generating answer (for debugging).

        Args:
            question: User's question
            top_k: Number of top chunks to return

        Returns:
            List of relevant chunks with metadata
        """
        try:
            if not self.chunks or not self.embeddings:
                if not self._load_index():
                    return []

            # Generate query embedding
            query_embedding = get_text_embedding(question)

            # Compute similarities
            similarities = []
            for i, chunk_embedding in enumerate(self.embeddings):
                similarity = cosine_similarity(query_embedding, chunk_embedding)
                similarities.append((i, similarity, self.chunks[i]))

            # Sort by similarity and get top k
            similarities.sort(key=lambda x: x[1], reverse=True)
            top_results = similarities[:top_k]

            # Format results
            results = []
            for i, (chunk_idx, similarity, chunk_text) in enumerate(top_results):
                results.append({
                    "rank": i + 1,
                    "chunk_index": chunk_idx,
                    "similarity": round(similarity, 4),
                    "content_preview": chunk_text[:200] + "..." if len(chunk_text) > 200 else chunk_text,
                    "full_content": chunk_text
                })

            return results

        except Exception as e:
            logger.error(f"Error getting relevant chunks: {e}")
            return []

    def get_session_info(self) -> Dict[str, Any]:
        """Get information about the current RAG session"""
        return {
            "session_id": self.session_id,
            "course_title": self.course_data.get('title', 'N/A') if self.course_data else 'N/A',
            "chunks_count": len(self.chunks),
            "embeddings_count": len(self.embeddings),
            "index_file": self.index_file,
            "index_exists": os.path.exists(f"temp/{self.index_file}")
        }


# Global RAG service registry
rag_services: Dict[str, RAGService] = {}


def get_rag_service(session_id: str) -> RAGService:
    """
    Get or create RAG service for session.

    Args:
        session_id: Session ID

    Returns:
        RAG service instance
    """
    if session_id not in rag_services:
        rag_services[session_id] = RAGService(session_id)

    return rag_services[session_id]


def create_rag_index(session_id: str, course_data: Dict[str, Any]) -> bool:
    """
    Create RAG index for a session.

    Args:
        session_id: Session ID
        course_data: Course data

    Returns:
        True if index created successfully
    """
    try:
        rag_service = get_rag_service(session_id)
        success = rag_service.load_course_data(course_data)

        if success:
            logger.info(f"Created RAG index for session: {session_id}")
        else:
            logger.error(f"Failed to create RAG index for session: {session_id}")

        return success

    except Exception as e:
        logger.error(f"Error creating RAG index: {e}")
        return False


def query_rag_index(session_id: str, question: str, top_k: int = 3) -> Tuple[str, List[str]]:
    """
    Query RAG index for a session.

    Args:
        session_id: Session ID
        question: User's question
        top_k: Number of top results

    Returns:
        Tuple of (answer, source_chunks)
    """
    try:
        rag_service = get_rag_service(session_id)
        return rag_service.query(question, top_k)

    except Exception as e:
        logger.error(f"Error querying RAG index: {e}")
        return f"Error processing question: {str(e)}", []


def cleanup_rag_session(session_id: str) -> bool:
    """
    Clean up RAG session resources.

    Args:
        session_id: Session ID

    Returns:
        True if cleanup successful
    """
    try:
        if session_id in rag_services:
            del rag_services[session_id]

        # Remove index file
        index_file = f"temp/rag_index_{session_id}.json"
        if os.path.exists(index_file):
            os.remove(index_file)

        logger.info(f"Cleaned up RAG session: {session_id}")
        return True

    except Exception as e:
        logger.error(f"Error cleaning up RAG session: {e}")
        return False
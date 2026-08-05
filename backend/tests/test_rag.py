import pytest
import os
import tempfile
from unittest.mock import patch, MagicMock
from app.services.rag_service import RAGService, get_rag_service, create_rag_index, query_rag_index


class TestRAGService:
    """Test cases for RAG (Retrieval Augmented Generation) service"""

    def setup_method(self):
        """Setup method run before each test"""
        # Create a mock course data for testing
        self.mock_course_data = {
            "title": "Python Programming Basics",
            "description": "Learn Python programming from scratch",
            "duration_weeks": 4,
            "learning_objectives": [
                "Understand Python syntax",
                "Learn data structures",
                "Master control flow",
                "Build simple applications"
            ],
            "prerequisites": ["Basic computer knowledge"],
            "weeks": [
                {
                    "week_number": 1,
                    "title": "Python Basics",
                    "objectives": ["Learn variables", "Understand data types"],
                    "days": [
                        {
                            "day_number": 1,
                            "title": "Introduction to Python",
                            "objectives": ["Install Python", "Write first program"],
                            "content": "Python is a high-level programming language...",
                            "activities": ["Install Python", "Write Hello World program"]
                        }
                    ]
                }
            ],
            "assignments": [
                {
                    "title": "Python Basics Quiz",
                    "type": "MCQ",
                    "difficulty": "beginner",
                    "questions": ["What is Python?", "How to install Python?"],
                    "solutions": ["Answer 1", "Answer 2"]
                }
            ],
            "flashcards": [
                {
                    "front": "What is Python?",
                    "back": "Python is a high-level programming language",
                    "category": "Concept"
                }
            ]
        }

    def test_rag_service_initialization(self):
        """Test RAG service initialization"""
        session_id = "test_session_123"
        rag_service = RAGService(session_id)

        assert rag_service.session_id == session_id
        assert rag_service.course_data is None
        assert rag_service.chunks == []
        assert rag_service.embeddings == []
        assert rag_service.index_file == "rag_index_test_session_123.json"

    def test_load_course_data(self):
        """Test loading course data into RAG service"""
        session_id = "test_session_123"
        rag_service = RAGService(session_id)

        # Load course data
        result = rag_service.load_course_data(self.mock_course_data)

        assert result is True
        assert rag_service.course_data == self.mock_course_data
        assert len(rag_service.chunks) > 0
        assert len(rag_service.embeddings) > 0
        assert len(rag_service.chunks) == len(rag_service.embeddings)

    def test_load_course_data_empty(self):
        """Test loading empty course data"""
        session_id = "test_session_123"
        rag_service = RAGService(session_id)

        result = rag_service.load_course_data({})
        assert result is False

    def test_extract_course_text(self):
        """Test course text extraction"""
        session_id = "test_session_123"
        rag_service = RAGService(session_id)
        rag_service.course_data = self.mock_course_data

        text = rag_service._extract_course_text()

        assert isinstance(text, str)
        assert len(text) > 0
        assert "Python Programming Basics" in text
        assert "Learn Python programming from scratch" in text

    def test_save_and_load_index(self):
        """Test saving and loading RAG index"""
        session_id = "test_session_123"
        rag_service = RAGService(session_id)

        # Load course data
        rag_service.load_course_data(self.mock_course_data)

        # Save index
        save_result = rag_service._save_index()
        assert save_result is True

        # Create new service and load index
        new_rag_service = RAGService(session_id)
        load_result = new_rag_service._load_index()

        assert load_result is True
        assert len(new_rag_service.chunks) == len(rag_service.chunks)
        assert len(new_rag_service.embeddings) == len(rag_service.embeddings)

    def test_query_rag_service(self):
        """Test querying RAG service"""
        session_id = "test_session_123"
        rag_service = RAGService(session_id)

        # Load course data
        rag_service.load_course_data(self.mock_course_data)

        # Query the service
        question = "What is Python?"
        answer, sources = rag_service.query(question, top_k=2)

        assert isinstance(answer, str)
        assert len(answer) > 0
        assert isinstance(sources, list)
        assert len(sources) <= 2

    def test_query_without_index(self):
        """Test querying RAG service without loaded index"""
        session_id = "test_session_123"
        rag_service = RAGService(session_id)

        # Query without loading data
        question = "What is Python?"
        answer, sources = rag_service.query(question, top_k=2)

        assert isinstance(answer, str)
        assert "Course data not available" in answer
        assert sources == []

    def test_get_relevant_chunks(self):
        """Test getting relevant chunks without generating answer"""
        session_id = "test_session_123"
        rag_service = RAGService(session_id)

        # Load course data
        rag_service.load_course_data(self.mock_course_data)

        # Get relevant chunks
        question = "What is Python?"
        chunks = rag_service.get_relevant_chunks(question, top_k=2)

        assert isinstance(chunks, list)
        assert len(chunks) <= 2

        if chunks:
            chunk = chunks[0]
            assert "rank" in chunk
            assert "chunk_index" in chunk
            assert "similarity" in chunk
            assert "content_preview" in chunk
            assert "full_content" in chunk

    def test_get_session_info(self):
        """Test getting session information"""
        session_id = "test_session_123"
        rag_service = RAGService(session_id)

        # Load course data
        rag_service.load_course_data(self.mock_course_data)

        # Get session info
        info = rag_service.get_session_info()

        assert isinstance(info, dict)
        assert info["session_id"] == session_id
        assert info["course_title"] == "Python Programming Basics"
        assert info["chunks_count"] == len(rag_service.chunks)
        assert info["embeddings_count"] == len(rag_service.embeddings)

    def test_global_rag_service_registry(self):
        """Test global RAG service registry"""
        session_id = "test_session_123"

        # Get service (should create new)
        service1 = get_rag_service(session_id)
        assert isinstance(service1, RAGService)

        # Get same service (should return existing)
        service2 = get_rag_service(session_id)
        assert service1 is service2

        # Get different service
        session_id2 = "test_session_456"
        service3 = get_rag_service(session_id2)
        assert service3 is not service1

    @patch('app.services.rag_service.create_rag_index')
    def test_create_rag_index_function(self, mock_create):
        """Test create_rag_index function"""
        mock_create.return_value = True

        result = create_rag_index("test_session_123", self.mock_course_data)
        assert result is True
        mock_create.assert_called_once_with("test_session_123", self.mock_course_data)

    @patch('app.services.rag_service.query_rag_index')
    def test_query_rag_index_function(self, mock_query):
        """Test query_rag_index function"""
        mock_query.return_value = ("Test answer", ["source1", "source2"])

        result = query_rag_index("test_session_123", "Test question")
        assert isinstance(result, tuple)
        assert result[0] == "Test answer"
        assert result[1] == ["source1", "source2"]

    def test_chunking_with_course_content(self):
        """Test that course content is properly chunked"""
        session_id = "test_session_123"
        rag_service = RAGService(session_id)

        # Load course data
        rag_service.load_course_data(self.mock_course_data)

        # Check that chunks were created
        assert len(rag_service.chunks) > 0

        # Check that chunks have reasonable size
        for chunk in rag_service.chunks:
            assert isinstance(chunk, str)
            assert len(chunk) > 0
            # Chunks should not be too large or too small
            assert len(chunk) < 2000
            assert len(chunk) > 50

    def test_embedding_generation(self):
        """Test that embeddings are generated for chunks"""
        session_id = "test_session_123"
        rag_service = RAGService(session_id)

        # Load course data
        rag_service.load_course_data(self.mock_course_data)

        # Check embeddings
        assert len(rag_service.embeddings) == len(rag_service.chunks)

        # Check embedding properties
        for embedding in rag_service.embeddings:
            assert isinstance(embedding, list)
            assert len(embedding) == 128  # Default embedding dimension
            assert all(isinstance(val, float) for val in embedding)

    def test_session_cleanup(self):
        """Test cleanup of session files"""
        session_id = "test_session_123"
        rag_service = RAGService(session_id)

        # Load course data and save index
        rag_service.load_course_data(self.mock_course_data)
        rag_service._save_index()

        # Check that index file was created
        index_file = f"temp/rag_index_{session_id}.json"
        assert os.path.exists(index_file)

        # Clean up (import the cleanup function)
        from app.services.rag_service import cleanup_rag_session
        result = cleanup_rag_service(session_id)

        assert result is True
        # Note: File might not be deleted if it doesn't exist in temp directory

    def test_fallback_content_extraction(self):
        """Test fallback content extraction when Course object fails"""
        session_id = "test_session_123"
        rag_service = RAGService(session_id)

        # Test with minimal course data that might fail Course object creation
        minimal_course_data = {
            "title": "Test Course",
            "description": "Test Description",
            "learning_objectives": ["Objective 1"],
            "prerequisites": ["Prerequisite 1"],
            "weeks": []
        }

        rag_service.course_data = minimal_course_data
        text = rag_service._extract_course_text()

        assert isinstance(text, str)
        assert "Test Course" in text
        assert "Test Description" in text

    def test_empty_course_data_handling(self):
        """Test handling of empty course data"""
        session_id = "test_session_123"
        rag_service = RAGService(session_id)

        # Test with empty course data
        rag_service.course_data = {}
        text = rag_service._extract_course_text()

        # Should return empty string or minimal content
        assert isinstance(text, str)

    def test_course_data_without_weeks(self):
        """Test course data without weeks structure"""
        session_id = "test_session_123"
        rag_service = RAGService(session_id)

        # Test with course data missing weeks
        incomplete_course_data = {
            "title": "Test Course",
            "description": "Test Description"
            # Missing weeks, objectives, etc.
        }

        result = rag_service.load_course_data(incomplete_course_data)
        # Should still work with fallback content extraction
        assert result is True
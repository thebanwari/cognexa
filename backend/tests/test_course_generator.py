import pytest
import json
from datetime import datetime
from app.services.llm_service import mock_llm_course_generator
from app.models.course_models import Course


class TestCourseGenerator:
    """Test cases for course generation service"""

    def test_mock_llm_course_generator_basic(self):
        """Test basic course generation"""
        course_data = mock_llm_course_generator(
            topic="Python Programming",
            duration=4,
            difficulty="beginner",
            language="english"
        )

        assert course_data is not None
        assert "course_id" in course_data
        assert "title" in course_data
        assert "description" in course_data
        assert "weeks" in course_data
        assert "assignments" in course_data
        assert "flashcards" in course_data

    def test_mock_llm_course_generator_duration_validation(self):
        """Test course generation with different durations"""
        # Test minimum duration
        course_data = mock_llm_course_generator(
            topic="Test Topic",
            duration=1,
            difficulty="beginner",
            language="english"
        )
        assert course_data["duration_weeks"] == 1

        # Test maximum duration
        course_data = mock_llm_course_generator(
            topic="Test Topic",
            duration=24,
            difficulty="beginner",
            language="english"
        )
        assert course_data["duration_weeks"] == 24

    def test_mock_llm_course_generator_difficulty_levels(self):
        """Test course generation with different difficulty levels"""
        difficulties = ["beginner", "intermediate", "advanced"]

        for difficulty in difficulties:
            course_data = mock_llm_course_generator(
                topic="Python Programming",
                duration=4,
                difficulty=difficulty,
                language="english"
            )

            assert course_data["difficulty"] == difficulty
            assert len(course_data["weeks"]) == 4
            assert len(course_data["learning_objectives"]) >= 4

    def test_mock_llm_course_generator_deterministic(self):
        """Test that course generation is deterministic for same inputs"""
        # Generate course twice with same parameters
        course_data1 = mock_llm_course_generator(
            topic="Python Programming",
            duration=4,
            difficulty="beginner",
            language="english"
        )

        course_data2 = mock_llm_course_generator(
            topic="Python Programming",
            duration=4,
            difficulty="beginner",
            language="english"
        )

        # Should be identical (deterministic)
        assert course_data1["course_id"] == course_data2["course_id"]
        assert course_data1["title"] == course_data2["title"]
        assert course_data1["description"] == course_data2["description"]

    def test_mock_llm_course_generator_different_topics(self):
        """Test course generation with different topics"""
        topics = ["Python Programming", "Web Development", "Machine Learning"]

        for topic in topics:
            course_data = mock_llm_course_generator(
                topic=topic,
                duration=4,
                difficulty="beginner",
                language="english"
            )

            assert topic.lower() in course_data["title"].lower()
            assert len(course_data["weeks"]) == 4

    def test_course_structure_validation(self):
        """Test that generated course has valid structure"""
        course_data = mock_llm_course_generator(
            topic="Python Programming",
            duration=4,
            difficulty="beginner",
            language="english"
        )

        # Validate course structure
        assert isinstance(course_data["course_id"], str)
        assert isinstance(course_data["title"], str)
        assert isinstance(course_data["description"], str)
        assert isinstance(course_data["duration_weeks"], int)
        assert isinstance(course_data["learning_objectives"], list)
        assert isinstance(course_data["prerequisites"], list)
        assert isinstance(course_data["weeks"], list)
        assert isinstance(course_data["assignments"], list)
        assert isinstance(course_data["flashcards"], list)

        # Validate weeks structure
        for week in course_data["weeks"]:
            assert "week_number" in week
            assert "title" in week
            assert "objectives" in week
            assert "days" in week
            assert isinstance(week["week_number"], int)
            assert isinstance(week["title"], str)
            assert isinstance(week["objectives"], list)
            assert isinstance(week["days"], list)

            # Validate days structure
            for day in week["days"]:
                assert "day_number" in day
                assert "title" in day
                assert "objectives" in day
                assert "content" in day
                assert "activities" in day
                assert isinstance(day["day_number"], int)
                assert isinstance(day["title"], str)
                assert isinstance(day["objectives"], list)
                assert isinstance(day["content"], str)
                assert isinstance(day["activities"], list)

    def test_course_content_extraction(self):
        """Test that course content can be extracted properly"""
        course_data = mock_llm_course_generator(
            topic="Python Programming",
            duration=4,
            difficulty="beginner",
            language="english"
        )

        # Convert to Course object and test content extraction
        course = Course(**course_data)
        content = course.get_total_content()

        assert isinstance(content, str)
        assert len(content) > 0
        assert course_data["title"] in content
        assert course_data["description"] in content

    def test_assignment_generation(self):
        """Test that assignments are generated correctly"""
        course_data = mock_llm_course_generator(
            topic="Python Programming",
            duration=4,
            difficulty="beginner",
            language="english"
        )

        assignments = course_data["assignments"]
        assert len(assignments) >= 1

        for assignment in assignments:
            assert "title" in assignment
            assert "type" in assignment
            assert "difficulty" in assignment
            assert "questions" in assignment
            assert isinstance(assignment["questions"], list)
            assert len(assignment["questions"]) > 0

    def test_flashcard_generation(self):
        """Test that flashcards are generated correctly"""
        course_data = mock_llm_course_generator(
            topic="Python Programming",
            duration=4,
            difficulty="beginner",
            language="english"
        )

        flashcards = course_data["flashcards"]
        assert len(flashcards) >= 1

        for flashcard in flashcards:
            assert "front" in flashcard
            assert "back" in flashcard
            assert "category" in flashcard
            assert isinstance(flashcard["front"], str)
            assert isinstance(flashcard["back"], str)
            assert isinstance(flashcard["category"], str)

    def test_course_id_uniqueness(self):
        """Test that different courses get different IDs"""
        course1 = mock_llm_course_generator(
            topic="Python Programming",
            duration=4,
            difficulty="beginner",
            language="english"
        )

        course2 = mock_llm_course_generator(
            topic="Web Development",
            duration=4,
            difficulty="beginner",
            language="english"
        )

        assert course1["course_id"] != course2["course_id"]

    def test_language_support(self):
        """Test course generation with different languages"""
        languages = ["english", "hindi"]

        for language in languages:
            course_data = mock_llm_course_generator(
                topic="Python Programming",
                duration=4,
                difficulty="beginner",
                language=language
            )

            assert course_data["language"] == language
            assert len(course_data["weeks"]) == 4
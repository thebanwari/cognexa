"""
Course Chain — LangChain chain that generates a complete course.

Architecture:
    CoursePrompt  →  GeminiLLM  →  CourseParser
                                      ↓
                                 Validated Dict
                                      ↓
                              (retry on failure)

Usage:
    chain = CourseChain()
    course_data = chain.generate(
        topic="Python Programming",
        duration=4,
        difficulty="beginner",
        language="english",
    )
"""

import logging
from typing import Dict, Any

from app.ai.providers.factory import get_provider
from app.ai.prompts.course_prompt import get_course_prompt
from app.ai.parsers.course_parser import parse_course_json, CourseParsingError
from app.config import GEMINI_MAX_RETRIES

logger = logging.getLogger(__name__)


class CourseChain:
    """
    LangChain chain: Prompt → LLM → Parser  with automatic retry on
    JSON parsing failures.

    The chain is stateless — every call to generate() is independent.
    Provider and prompt are resolved once at construction time.
    """

    def __init__(self):
        provider = get_provider()
        self._llm = provider.get_llm()
        self._prompt = get_course_prompt()
        self._max_retries = GEMINI_MAX_RETRIES
        logger.info("CourseChain initialised")

    def generate(
        self,
        topic: str,
        duration: int,
        difficulty: str,
        language: str,
    ) -> Dict[str, Any]:
        """
        Generate a complete course via LLM.

        Args:
            topic:      Course subject (e.g. "Python Programming")
            duration:   Duration in weeks (1-24)
            difficulty: "beginner" | "intermediate" | "advanced"
            language:   "english" | "hindi"

        Returns:
            A validated course dictionary matching the existing schema:
            {title, description, learning_objectives, prerequisites,
             weeks: [{week_number, title, objectives, days: [...]}],
             assignments: [...], flashcards: [...]}

        Raises:
            CourseParsingError: If all retry attempts fail to produce valid JSON.
            Exception: If the LLM call itself fails (network, auth, quota).
        """
        chain = self._prompt | self._llm

        last_error = None

        for attempt in range(1, self._max_retries + 1):
            try:
                logger.info(
                    f"CourseChain.generate() attempt {attempt}/{self._max_retries} "
                    f"— topic='{topic}', duration={duration}, "
                    f"difficulty={difficulty}, language={language}"
                )

                result = chain.invoke({
                    "topic": topic,
                    "duration": str(duration),
                    "difficulty": difficulty,
                    "language": language,
                })

                raw_text = result.content

                course_data = parse_course_json(raw_text)

                logger.info(
                    f"Course generated successfully on attempt {attempt}: "
                    f"'{course_data.get('title', 'Untitled')}'"
                )
                return course_data

            except CourseParsingError as e:
                last_error = e
                logger.warning(
                    f"Attempt {attempt}/{self._max_retries} failed — "
                    f"JSON parsing error: {e}"
                )
                # Continue to next retry

            except Exception as e:
                # Non-parsing errors (network, auth, quota) — don't retry
                logger.error(f"LLM call failed (non-retriable): {e}")
                raise

        # All retries exhausted
        raise CourseParsingError(
            f"Failed to generate valid course JSON after "
            f"{self._max_retries} attempts. Last error: {last_error}"
        )

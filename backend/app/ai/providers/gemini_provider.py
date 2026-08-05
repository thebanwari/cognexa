"""
Gemini Provider — wraps Google Gemini via langchain-google-genai.

Usage:
    provider = GeminiProvider()
    llm = provider.get_llm()
"""

import logging
from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    GEMINI_TEMPERATURE,
    GEMINI_MAX_OUTPUT_TOKENS,
)

logger = logging.getLogger(__name__)


class GeminiProvider:
    """Wraps ChatGoogleGenerativeAI with project-level defaults."""

    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY is not set. "
                "Add it to your .env file or set the environment variable."
            )

        self._llm = ChatGoogleGenerativeAI(
            model=GEMINI_MODEL,
            google_api_key=GEMINI_API_KEY,
            temperature=GEMINI_TEMPERATURE,
            max_output_tokens=GEMINI_MAX_OUTPUT_TOKENS,
            convert_system_message_to_human=True,
            response_mime_type="application/json",
        )
        logger.info(
            f"GeminiProvider initialised — model={GEMINI_MODEL}, "
            f"temperature={GEMINI_TEMPERATURE}, "
            f"max_tokens={GEMINI_MAX_OUTPUT_TOKENS}"
        )

    def get_llm(self) -> ChatGoogleGenerativeAI:
        """Return the configured LLM instance."""
        return self._llm

"""
Provider Factory — returns the correct LLM provider based on config.

Usage:
    provider = get_provider()
    llm = provider.get_llm()
"""

import logging
from app.config import LLM_PROVIDER

logger = logging.getLogger(__name__)


def get_provider():
    """
    Return an LLM provider instance based on the LLM_PROVIDER config value.

    Currently supported:
        - "gemini" → GeminiProvider (Google Gemini via langchain-google-genai)

    Raises:
        ValueError: If the provider name is unrecognised.
    """
    provider_name = LLM_PROVIDER.lower().strip()

    if provider_name == "gemini":
        from app.ai.providers.gemini_provider import GeminiProvider
        logger.info("Creating GeminiProvider")
        return GeminiProvider()
    else:
        raise ValueError(
            f"Unknown LLM provider: '{provider_name}'. "
            f"Supported providers: gemini"
        )

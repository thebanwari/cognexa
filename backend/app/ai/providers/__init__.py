"""LLM Provider wrappers — one module per provider."""

from app.ai.providers.factory import get_provider

__all__ = ["get_provider"]

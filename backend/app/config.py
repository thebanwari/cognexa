import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
DEFAULT_SESSION_TTL = int(os.getenv("SESSION_TTL", "86400"))  # 24 hours in seconds
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "mock-embedding")

# ── Gemini / LangChain Configuration ────────────────────────
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
GEMINI_TEMPERATURE = float(os.getenv("GEMINI_TEMPERATURE", "0.7"))
GEMINI_MAX_OUTPUT_TOKENS = int(os.getenv("GEMINI_MAX_OUTPUT_TOKENS", "32768"))
GEMINI_MAX_RETRIES = int(os.getenv("GEMINI_MAX_RETRIES", "3"))
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")

# When True, always use deterministic mock even if GEMINI_API_KEY is set.
# When False (default), use real AI if GEMINI_API_KEY is available.
USE_MOCK_LLM = os.getenv("USE_MOCK_LLM", "false").lower() == "true"

# PDF Configuration
PDF_OUTPUT_DIR = "app/static/pdf"
TEMPLATE_DIR = "app/templates"

# RAG Configuration
CHUNK_SIZE = 700  # characters
CHUNK_OVERLAP = 100  # characters
TOP_K_CHUNKS = 3  # number of chunks to retrieve

# Session Configuration
SESSION_CLEANUP_INTERVAL = 3600  # 1 hour in seconds
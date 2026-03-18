import os
from pathlib import Path

from dotenv import load_dotenv


def get_api_key() -> str:
    """Load and validate the Gemini API key from .env file."""
    env_path = Path.cwd() / ".env"
    load_dotenv(env_path)

    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise SystemExit(
            "Error: GEMINI_API_KEY is not set.\n"
            "1. Copy .env.example to .env\n"
            "2. Add your Gemini API key to .env\n"
            "   GEMINI_API_KEY=your_key_here"
        )
    return api_key

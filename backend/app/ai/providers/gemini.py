from google import genai

from app.core.config import settings


class GeminiProvider:
    """Wrapper around the Gemini SDK."""

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )
        self.model = settings.GEMINI_MODEL
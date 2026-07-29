from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    PROJECT_NAME = "StudioPilot AI"
    API_VERSION = "0.1.0"

    DATABASE_URL = os.getenv("DATABASE_URL")

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    GEMINI_MODEL = os.getenv(
        "GEMINI_MODEL",
        "gemini-2.5-flash"
    )


settings = Settings()
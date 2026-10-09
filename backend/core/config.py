from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    APP_NAME = os.getenv("APP_NAME", "Welfare AI")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

    # MongoDB
    MONGODB_URI = os.getenv("MONGODB_URI")

    # LLM configuration
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    LLM_MODEL = os.getenv("LLM_MODEL", "qwen/qwen3.8-27b")


settings = Settings()
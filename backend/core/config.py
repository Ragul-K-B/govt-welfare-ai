from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    APP_NAME = os.getenv("APP_NAME", "Welfare AI")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    MONGODB_URI = os.getenv("MONGODB_URI")


settings = Settings()
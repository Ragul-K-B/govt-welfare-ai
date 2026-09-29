from fastapi import FastAPI
from core.config import settings
from db.mongodb import client

app = FastAPI(title=settings.APP_NAME)


@app.get("/")
def root():
    return {
        "message": "Welfare AI backend is running",
        "environment": settings.ENVIRONMENT
    }


@app.get("/db-test")
def database_test():
    client.admin.command("ping")

    return {
        "message": "MongoDB connection successful"
    }
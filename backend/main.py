
from fastapi import FastAPI

from core.config import settings
from db.mongodb import client
from api.routes import router as welfare_router


app = FastAPI(title=settings.APP_NAME)

# Register the welfare discovery endpoints
app.include_router(welfare_router)


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

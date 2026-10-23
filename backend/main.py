
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from db.mongodb import client
from api.routes import router as welfare_router


app = FastAPI(title=settings.APP_NAME)

# Allow requests from the deployed frontend and local development frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://govt-welfare-ai.vercel.app",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from services.discovery import discover_schemes
from services.conversation import continue_discovery

router = APIRouter(prefix="/api", tags=["Welfare AI"])


class DiscoverRequest(BaseModel):
    message: str = Field(min_length=1)
    top_k: int = Field(default=5, ge=1, le=20)
    existing_profile: dict = Field(default_factory=dict)


class ContinueRequest(BaseModel):
    original_message: str
    answer_message: str = Field(min_length=1)
    citizen_profile: dict
    pending_questions: list[dict]
    top_k: int = Field(default=5, ge=1, le=20)


@router.post("/discover")
def discover(request: DiscoverRequest):
    try:
        return discover_schemes(
            message=request.message,
            top_k=request.top_k,
            existing_profile=request.existing_profile
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Discovery failed: {str(error)}"
        ) from error


@router.post("/continue")
def continue_conversation(request: ContinueRequest):
    try:
        return continue_discovery(
            original_message=request.original_message,
            answer_message=request.answer_message,
            citizen_profile=request.citizen_profile,
            pending_questions=request.pending_questions,
            top_k=request.top_k
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Conversation continuation failed: {str(error)}"
        ) from error

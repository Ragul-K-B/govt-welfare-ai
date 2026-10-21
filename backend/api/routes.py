from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from services.chat import handle_chat
from db.mongodb import schemes_collection
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

class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    citizen_profile: dict = Field(default_factory=dict)
    pending_questions: list[dict] = Field(default_factory=list)
    last_result: dict | None = None
    active_search: str | None = None
    conversation_context: list[dict] = Field(default_factory=list)
    top_k: int = Field(default=5, ge=1, le=20)


@router.post("/chat")
def chat(request: ChatRequest):
    try:
        return handle_chat(
            message=request.message,
            citizen_profile=request.citizen_profile,
            pending_questions=request.pending_questions,
            last_result=request.last_result,
            active_search=request.active_search,
            conversation_context=request.conversation_context,
            top_k=request.top_k,
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Chat request failed: {str(error)}"
        ) from error

@router.get("/schemes")
def browse_schemes(
    search: str = "",
    limit: int = 20
):
    try:
        limit = max(1, min(limit, 50))

        query = {}

        if search.strip():
            query["name"] = {
                "$regex": search.strip(),
                "$options": "i"
            }

        projection = {
            "_id": 0,
            "scheme_id": 1,
            "name": 1,
            "description": 1,
            "benefits": 1,
            "documents": 1,
            "application": 1,
            "eligibility": 1,
            "sources": 1,
            "metadata": 1,
        }

        schemes = list(
            schemes_collection.find(
                query,
                projection
            ).limit(limit)
        )

        return {
            "count": len(schemes),
            "schemes": schemes
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to browse schemes: {str(error)}"
        ) from error
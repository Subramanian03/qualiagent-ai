from fastapi import APIRouter

from backend.ai.settings import (
    load_ai_settings,
)
from backend.models.ai_status import (
    AIStatusResponse,
)


router = APIRouter(
    prefix="/api/ai",
    tags=["AI"]
)


@router.get(
    "/status",
    response_model=AIStatusResponse
)
def get_ai_status():

    settings = load_ai_settings()

    return AIStatusResponse(
        mode=settings.mode,
        provider=settings.provider,
        model=settings.model,
        real_provider_ready=(
    settings.mode == "real"
    and settings.provider == "groq"
    and bool(settings.model)
    and bool(settings.groq_api_key)
)
    )
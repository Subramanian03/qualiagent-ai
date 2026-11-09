from pydantic import BaseModel


class AIStatusResponse(BaseModel):

    mode: str
    provider: str
    model: str | None
    real_provider_ready: bool
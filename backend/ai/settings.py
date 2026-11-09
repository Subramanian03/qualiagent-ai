import os

from dataclasses import dataclass

from backend.ai.errors import (
    AIProviderConfigurationError,
)


VALID_AI_MODES = {
    "mock",
    "real",
}


@dataclass(frozen=True)
class AISettings:

    mode: str
    provider: str
    model: str | None

    groq_api_key: str | None

    request_timeout_seconds: int
    max_retries: int


def get_optional_environment_value(
    name: str
) -> str | None:

    value = os.getenv(
        name
    )

    if value is None:
        return None

    stripped = value.strip()

    return stripped or None


def get_integer_environment_value(
    name: str,
    default: int
) -> int:

    raw_value = (
        get_optional_environment_value(
            name
        )
    )

    if raw_value is None:
        return default

    try:
        value = int(
            raw_value
        )

    except ValueError as exc:
        raise AIProviderConfigurationError(
            f"{name} must be an integer"
        ) from exc

    if value < 0:
        raise AIProviderConfigurationError(
            f"{name} cannot be negative"
        )

    return value


def load_ai_settings() -> AISettings:

    mode = (
        get_optional_environment_value(
            "AI_MODE"
        )
        or "mock"
    ).lower()

    provider = (
        get_optional_environment_value(
            "AI_PROVIDER"
        )
        or "mock"
    ).lower()

    model = (
        get_optional_environment_value(
            "AI_MODEL"
        )
    )

    groq_api_key = (
      get_optional_environment_value(
        "GROQ_API_KEY"
     )
   )

    azure_endpoint = (
       get_optional_environment_value(
        "AZURE_OPENAI_ENDPOINT"
    )
)

    azure_api_key = (
       get_optional_environment_value(
        "AZURE_OPENAI_API_KEY"
    )
)

    if mode not in VALID_AI_MODES:
        raise AIProviderConfigurationError(
            "AI_MODE must be 'mock' or 'real'"
        )

    if mode == "mock":
        provider = "mock"

    if mode == "real":

        if provider == "mock":
            raise AIProviderConfigurationError(
                "AI_PROVIDER cannot be 'mock' "
                "when AI_MODE is 'real'"
            )

        if not model:
            raise AIProviderConfigurationError(
                "AI_MODEL is required when "
                "AI_MODE is 'real'"
            )

        if provider == "groq":

         if not groq_api_key:
           raise AIProviderConfigurationError(
            "GROQ_API_KEY is required "
            "when using Groq"
        )
        
        if provider == "azure_openai":

          if not azure_endpoint:
            raise AIProviderConfigurationError(
            "AZURE_OPENAI_ENDPOINT is "
            "required for Azure OpenAI"
        )

          if not azure_api_key:
            raise AIProviderConfigurationError(
            "AZURE_OPENAI_API_KEY is "
            "required for Azure OpenAI"
        )

    return AISettings(
    mode=mode,
    provider=provider,
    model=model,
    groq_api_key=groq_api_key,
    request_timeout_seconds=(
        get_integer_environment_value(
            "AI_REQUEST_TIMEOUT_SECONDS",
            90
        )
    ),
    max_retries=(
        get_integer_environment_value(
            "AI_MAX_RETRIES",
            2
        )
    )
)
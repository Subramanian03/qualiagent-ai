from backend.ai.errors import (
    AIProviderConfigurationError,
)

from backend.ai.groq_provider import (
    GroqAIProvider,
)

from backend.ai.mock_provider import (
    MockAIProvider,
)

from backend.ai.provider import (
    AIProvider,
)

from backend.ai.settings import (
    load_ai_settings,
)


def get_ai_provider() -> AIProvider:

    settings = load_ai_settings()

    if settings.mode == "mock":
        return MockAIProvider()

    if (
        settings.mode == "real" and
        settings.provider == "groq"
    ):
        return GroqAIProvider(
            settings
        )

    raise AIProviderConfigurationError(
        "Unsupported real AI provider: "
        f"{settings.provider}"
    )
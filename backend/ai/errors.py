class AIProviderError(RuntimeError):
    """Base error for AI provider failures."""


class AIProviderConfigurationError(
    AIProviderError
):
    """Raised when AI configuration is invalid."""


class AIProviderResponseError(
    AIProviderError
):
    """Raised when an AI response is invalid."""


class AIProviderUnavailableError(
    AIProviderError
):
    """Raised when a provider cannot be reached."""
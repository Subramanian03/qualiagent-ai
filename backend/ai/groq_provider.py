import json

from typing import Any

from openai import APIConnectionError
from openai import APIStatusError
from openai import OpenAI
from openai import RateLimitError

from backend.ai.errors import (
    AIProviderConfigurationError,
    AIProviderResponseError,
    AIProviderUnavailableError,
)

from backend.ai.provider import (
    AIProvider,
)

from backend.ai.settings import (
    AISettings,
)


class GroqAIProvider(AIProvider):

    def __init__(
        self,
        settings: AISettings
    ):

        if not settings.groq_api_key:
            raise AIProviderConfigurationError(
                "Groq API key is missing"
            )

        if not settings.model:
            raise AIProviderConfigurationError(
                "Groq model is missing"
            )

        self.settings = settings

        self.client = OpenAI(
            api_key=settings.groq_api_key,
            base_url=(
                "https://api.groq.com/"
                "openai/v1"
            ),
            timeout=(
                settings
                .request_timeout_seconds
            ),
            max_retries=(
                settings.max_retries
            )
        )


    def generate(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        task: str
    ) -> dict[str, Any]:

        if not system_prompt.strip():
            raise AIProviderResponseError(
                "System prompt cannot be empty"
            )

        if not user_prompt.strip():
            raise AIProviderResponseError(
                "User prompt cannot be empty"
            )

        task_instruction = (
            "\n\n"
            "Return exactly one valid JSON "
            "object. Do not use Markdown "
            "code fences. Do not include "
            "text outside the JSON object. "
            f"Task: {task}."
        )

        try:

            completion = (
                self.client
                .chat
                .completions
                .create(
                    model=(
                        self.settings.model
                    ),
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                system_prompt
                                + task_instruction
                            )
                        },
                        {
                            "role": "user",
                            "content":
                                user_prompt
                        }
                    ]
                )
            )

        except RateLimitError as exc:
            raise AIProviderUnavailableError(
                "Groq rate limit reached"
            ) from exc

        except APIConnectionError as exc:
            raise AIProviderUnavailableError(
                "Unable to connect to Groq"
            ) from exc

        except APIStatusError as exc:
            raise AIProviderUnavailableError(
                "Groq request failed with "
                f"status {exc.status_code}"
            ) from exc

        except Exception as exc:
            raise AIProviderUnavailableError(
                "Unexpected Groq "
                "provider failure"
            ) from exc


        if not completion.choices:
            raise AIProviderResponseError(
                "Groq returned no response"
            )


        content = (
            completion
            .choices[0]
            .message
            .content
        )


        if not content:
            raise AIProviderResponseError(
                "Groq returned empty content"
            )


        try:

            parsed = json.loads(
                content
            )

        except json.JSONDecodeError as exc:
            raise AIProviderResponseError(
                "Groq did not return "
                "valid JSON"
            ) from exc


        if not isinstance(
            parsed,
            dict
        ):
            raise AIProviderResponseError(
                "Groq response must be "
                "a JSON object"
            )


        return parsed
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
from backend.ai.provider import AIProvider
from backend.ai.settings import AISettings


class AzureOpenAIProvider(AIProvider):

    def __init__(
        self,
        settings: AISettings
    ):

        if not settings.azure_endpoint:
            raise AIProviderConfigurationError(
                "Azure OpenAI endpoint "
                "is missing"
            )

        if not settings.azure_api_key:
            raise AIProviderConfigurationError(
                "Azure OpenAI API key "
                "is missing"
            )

        if not settings.model:
            raise AIProviderConfigurationError(
                "Azure OpenAI deployment "
                "name is missing"
            )

        self.settings = settings

        endpoint = (
            settings.azure_endpoint
            .rstrip("/")
        )

        if not endpoint.endswith(
            "/openai/v1"
        ):
            endpoint = (
                f"{endpoint}/openai/v1"
            )

        self.client = OpenAI(
            api_key=(
                settings.azure_api_key
            ),
            base_url=(
                f"{endpoint}/"
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

        if not task.strip():
            raise AIProviderResponseError(
                "AI task cannot be empty"
            )

        task_instruction = (
            "\n\n"
            "Return one valid JSON object only. "
            "Do not include Markdown fences, "
            "commentary, or text outside JSON. "
            f"QualiAgent task: {task}."
        )

        try:

            completion = (
                self.client
                .chat
                .completions
                .create(
                    model=self.settings.model,
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
                            "content": user_prompt
                        }
                    ],
                    response_format={
                        "type": "json_object"
                    }
                )
            )

        except RateLimitError as exc:

            raise AIProviderUnavailableError(
                "Azure OpenAI rate limit "
                "was reached"
            ) from exc

        except APIConnectionError as exc:

            raise AIProviderUnavailableError(
                "Unable to connect to "
                "Azure OpenAI"
            ) from exc

        except APIStatusError as exc:

            raise AIProviderUnavailableError(
                "Azure OpenAI request failed "
                f"with status {exc.status_code}"
            ) from exc

        except Exception as exc:

            raise AIProviderUnavailableError(
                "Unexpected Azure OpenAI "
                "provider failure"
            ) from exc


        if not completion.choices:

            raise AIProviderResponseError(
                "Azure OpenAI returned "
                "no choices"
            )


        content = (
            completion
            .choices[0]
            .message
            .content
        )


        if not content:

            raise AIProviderResponseError(
                "Azure OpenAI returned "
                "an empty response"
            )


        try:

            parsed = json.loads(
                content
            )

        except json.JSONDecodeError as exc:

            raise AIProviderResponseError(
                "Azure OpenAI returned "
                "invalid JSON"
            ) from exc


        if not isinstance(
            parsed,
            dict
        ):

            raise AIProviderResponseError(
                "Azure OpenAI response "
                "must be a JSON object"
            )


        return parsed
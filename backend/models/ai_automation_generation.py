from typing import Literal

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import field_validator
from pydantic import model_validator


AutomationFramework = Literal[
    "playwright",
]


AutomationLanguage = Literal[
    "javascript",
]


class AIAutomationGeneration(
    BaseModel
):

    model_config = ConfigDict(
        extra="forbid"
    )

    test_case_id: str = Field(
        min_length=3,
        max_length=150
    )

    framework: AutomationFramework

    language: AutomationLanguage

    code: str = Field(
        min_length=20,
        max_length=100000
    )

    used_inputs: list[str] = Field(
        default_factory=list,
        max_length=50
    )


    @field_validator(
        "test_case_id",
        "code",
        mode="before"
    )
    @classmethod
    def clean_required_text(
        cls,
        value
    ):

        if isinstance(value, str):
            return value.strip()

        return value


    @field_validator(
        "framework",
        "language",
        mode="before"
    )
    @classmethod
    def normalise_enum_value(
        cls,
        value
    ):

        if isinstance(value, str):
            return (
                value
                .strip()
                .lower()
            )

        return value


    @field_validator(
        "used_inputs",
        mode="before"
    )
    @classmethod
    def normalise_input_keys(
        cls,
        value
    ):

        if value is None:
            return []

        if not isinstance(
            value,
            list
        ):
            return value


        cleaned = []

        for item in value:

            if not isinstance(
                item,
                str
            ):
                cleaned.append(
                    item
                )

                continue


            key = (
                item
                .strip()
                .upper()
            )


            if (
                key and
                key not in cleaned
            ):
                cleaned.append(
                    key
                )


        return cleaned


    @model_validator(
        mode="after"
    )
    def validate_code_contract(
        self
    ):

        code = self.code


        required_markers = [
            "@playwright/test",
            "test(",
        ]


        for marker in required_markers:

            if marker not in code:

                raise ValueError(
                    "Generated automation code "
                    "is missing required "
                    f"Playwright marker: "
                    f"{marker}"
                )


        return self
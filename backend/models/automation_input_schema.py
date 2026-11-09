import re

from typing import Literal

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import field_validator
from pydantic import model_validator


AutomationInputType = Literal[
    "text",
    "password",
    "url",
    "number",
    "email",
    "boolean",
    "textarea",
]


AutomationInputScope = Literal[
    "project",
    "execution",
]


class AutomationInputDefinition(
    BaseModel
):

    model_config = ConfigDict(
        extra="forbid"
    )

    key: str = Field(
        min_length=2,
        max_length=100
    )

    label: str = Field(
        min_length=2,
        max_length=150
    )

    input_type: AutomationInputType

    required: bool = True

    secret: bool = False

    scope: AutomationInputScope = (
        "execution"
    )

    description: str = Field(
        min_length=5,
        max_length=1000
    )

    placeholder: str | None = Field(
        default=None,
        max_length=200
    )


    @field_validator(
        "key",
        mode="before"
    )
    @classmethod
    def normalise_key(
        cls,
        value
    ):

        if not isinstance(value, str):
            return value

        value = (
            value
            .strip()
            .upper()
        )

        value = re.sub(
            r"[^A-Z0-9_]",
            "_",
            value
        )

        value = re.sub(
            r"_+",
            "_",
            value
        )

        return value.strip("_")


    @field_validator(
        "key"
    )
    @classmethod
    def validate_key(
        cls,
        value
    ):

        if not re.fullmatch(
            r"[A-Z][A-Z0-9_]*",
            value
        ):
            raise ValueError(
                "Automation input key must "
                "use environment-variable "
                "format"
            )

        return value


    @field_validator(
        "label",
        "description",
        "placeholder",
        mode="before"
    )
    @classmethod
    def clean_text(
        cls,
        value
    ):

        if isinstance(value, str):
            cleaned = value.strip()

            return (
                cleaned
                if cleaned
                else None
            )

        return value


    @model_validator(
        mode="after"
    )
    def validate_secret_rules(
        self
    ):

        if (
            self.input_type ==
            "password" and
            not self.secret
        ):
            raise ValueError(
                "Password inputs must "
                "be marked secret"
            )

        if (
            self.secret and
            self.scope != "execution"
        ):
            raise ValueError(
                "Secret inputs must use "
                "execution scope"
            )

        return self


class AutomationInputSchema(
    BaseModel
):

    model_config = ConfigDict(
        extra="forbid"
    )

    test_case_id: str = Field(
        min_length=3,
        max_length=150
    )

    inputs: list[
        AutomationInputDefinition
    ] = Field(
        default_factory=list,
        max_length=50
    )


    @field_validator(
        "test_case_id",
        mode="before"
    )
    @classmethod
    def clean_test_case_id(
        cls,
        value
    ):

        if isinstance(value, str):
            return value.strip()

        return value


    @model_validator(
        mode="after"
    )
    def validate_unique_keys(
        self
    ):

        keys = [
            item.key
            for item in self.inputs
        ]

        if len(keys) != len(set(keys)):
            raise ValueError(
                "Automation input keys "
                "must be unique"
            )

        return self
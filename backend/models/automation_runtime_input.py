import re

from typing import Any

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import field_validator


class AutomationRuntimeInputSubmission(
    BaseModel
):

    model_config = ConfigDict(
        extra="forbid"
    )

    values: dict[
        str,
        Any
    ] = Field(
        default_factory=dict
    )


    @field_validator(
        "values"
    )
    @classmethod
    def validate_input_keys(
        cls,
        values
    ):

        cleaned = {}

        for key, value in values.items():

            if not isinstance(key, str):
                raise ValueError(
                    "Automation input keys "
                    "must be strings"
                )


            normalised_key = (
                key
                .strip()
                .upper()
            )


            if not re.fullmatch(
                r"[A-Z][A-Z0-9_]*",
                normalised_key
            ):
                raise ValueError(
                    "Automation input key "
                    f"'{key}' is invalid"
                )


            if normalised_key in cleaned:
                raise ValueError(
                    "Duplicate automation "
                    f"input key '{normalised_key}'"
                )


            cleaned[
                normalised_key
            ] = value


        return cleaned

class ValidatedAutomationRuntimeInputs(
    BaseModel
):

    model_config = ConfigDict(
        extra="forbid"
    )

    non_secret_values: dict[
        str,
        Any
    ] = Field(
        default_factory=dict
    )

    secret_values: dict[
        str,
        str
    ] = Field(
        default_factory=dict
    )
from typing import Any
from typing import Literal

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import field_validator
from pydantic import model_validator


class ManualCycleResultUpdate(
    BaseModel
):

    model_config = ConfigDict(
        extra="forbid"
    )


    status: Literal[
        "passed",
        "failed",
        "blocked",
        "skipped",
    ]


    actual_result: str | None = Field(
        default=None,
        max_length=5000
    )


    comment: str | None = Field(
        default=None,
        max_length=2000
    )


    defect_reference: str | None = Field(
        default=None,
        max_length=200
    )


    @field_validator(
        "actual_result",
        "comment",
        "defect_reference",
        mode="before"
    )
    @classmethod
    def clean_optional_text(
        cls,
        value
    ):

        if value is None:
            return None


        cleaned = str(
            value
        ).strip()


        return (
            cleaned
            if cleaned
            else None
        )


    @model_validator(
        mode="after"
    )
    def validate_result_details(
        self
    ):

        if (
            self.status == "failed"
            and
            not self.actual_result
        ):

            raise ValueError(
                "Actual result is required "
                "when a Manual Cycle item "
                "is marked as failed"
            )


        if (
            self.status == "blocked"
            and
            not self.comment
        ):

            raise ValueError(
                "Comment is required when "
                "a Manual Cycle item is "
                "marked as blocked"
            )


        return self


class AutomatedCycleRunRequest(
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
    def validate_values(
        cls,
        value
    ):

        if not isinstance(
            value,
            dict
        ):

            raise ValueError(
                "Runtime values must be "
                "provided as an object"
            )


        cleaned = {}


        for key, runtime_value in (
            value.items()
        ):

            cleaned_key = str(
                key or ""
            ).strip()


            if not cleaned_key:

                raise ValueError(
                    "Runtime input keys "
                    "cannot be empty"
                )


            if len(cleaned_key) > 200:

                raise ValueError(
                    "Runtime input keys cannot "
                    "exceed 200 characters"
                )


            cleaned[
                cleaned_key
            ] = runtime_value


        return cleaned
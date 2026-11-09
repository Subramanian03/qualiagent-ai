from typing import Literal

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import field_validator


RiskLevel = Literal[
    "low",
    "medium",
    "high",
    "critical",
]


ApplicationType = Literal[
    "web",
    "mobile",
    "api",
    "desktop",
    "other",
]


SuggestedTestType = Literal[
    "positive",
    "negative",
    "boundary",
    "validation",
    "functional",
    "integration",
    "security",
    "performance",
    "accessibility",
    "usability",
    "compatibility",
]


class AIRequirementAnalysis(BaseModel):

    model_config = ConfigDict(
        extra="forbid"
    )

    testable: bool

    risk_level: RiskLevel

    application_type: ApplicationType

    summary: str = Field(
        min_length=10,
        max_length=2000
    )

    identified_keywords: list[str] = (
        Field(
            default_factory=list,
            max_length=25
        )
    )

    suggested_test_types: list[
        SuggestedTestType
    ] = Field(
        default_factory=list,
        max_length=12
    )

    acceptance_criteria: list[str] = (
        Field(
            default_factory=list,
            max_length=30
        )
    )

    questions: list[str] = Field(
        default_factory=list,
        max_length=20
    )


    @field_validator(
        "risk_level",
        "application_type",
        mode="before"
    )
    @classmethod
    def normalise_enum_value(
        cls,
        value
    ):

        if isinstance(value, str):
            return value.strip().lower()

        return value


    @field_validator(
        "identified_keywords",
        "suggested_test_types",
        mode="before"
    )
    @classmethod
    def normalise_short_list(
        cls,
        value
    ):

        if value is None:
            return []

        if not isinstance(value, list):
            return value

        normalised = []

        for item in value:

            if not isinstance(item, str):
                normalised.append(item)
                continue

            cleaned = (
                item
                .strip()
                .lower()
            )

            if (
                cleaned and
                cleaned not in normalised
            ):
                normalised.append(
                    cleaned
                )

        return normalised


    @field_validator(
        "acceptance_criteria",
        "questions",
        mode="before"
    )
    @classmethod
    def clean_text_list(
        cls,
        value
    ):

        if value is None:
            return []

        if not isinstance(value, list):
            return value

        cleaned_items = []

        for item in value:

            if not isinstance(item, str):
                cleaned_items.append(item)
                continue

            cleaned = item.strip()

            if (
                cleaned and
                cleaned not in cleaned_items
            ):
                cleaned_items.append(
                    cleaned
                )

        return cleaned_items


    @field_validator(
        "summary",
        mode="before"
    )
    @classmethod
    def clean_summary(
        cls,
        value
    ):

        if isinstance(value, str):
            return value.strip()

        return value
from typing import Literal

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import field_validator
from pydantic import model_validator


AITestType = Literal[
    "positive",
    "negative",
    "boundary",
    "validation",
    "functional",
    "integration",
    "security",
    "performance",
    "accessibility",
]


AITestPriority = Literal[
    "low",
    "medium",
    "high",
    "critical",
]


class AITestStep(BaseModel):

    model_config = ConfigDict(
        extra="forbid"
    )

    step_number: int = Field(
        ge=1,
        le=100
    )

    action: str = Field(
        min_length=3,
        max_length=2000
    )

    expected_result: str = Field(
        min_length=3,
        max_length=2000
    )


    @field_validator(
        "action",
        "expected_result",
        mode="before"
    )
    @classmethod
    def clean_step_text(
        cls,
        value
    ):

        if isinstance(value, str):
            return value.strip()

        return value


class AITestCase(BaseModel):

    model_config = ConfigDict(
        extra="forbid"
    )

    test_case_id: str = Field(
        min_length=3,
        max_length=150
    )

    title: str = Field(
        min_length=3,
        max_length=255
    )

    test_type: AITestType

    priority: AITestPriority

    preconditions: list[str] = Field(
        default_factory=list,
        max_length=30
    )

    test_data: list[str] = Field(
        default_factory=list,
        max_length=30
    )

    steps: list[AITestStep] = Field(
        min_length=1,
        max_length=100
    )

    automation_candidate: bool


    @field_validator(
        "test_case_id",
        "title",
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
        "test_type",
        "priority",
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
        "preconditions",
        "test_data",
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

        cleaned = []

        for item in value:

            if not isinstance(item, str):
                cleaned.append(item)
                continue

            text = item.strip()

            if (
                text and
                text not in cleaned
            ):
                cleaned.append(text)

        return cleaned


    @model_validator(
        mode="after"
    )
    def validate_step_numbers(
        self
    ):

        actual = [
            step.step_number
            for step in self.steps
        ]

        expected = list(
            range(
                1,
                len(self.steps) + 1
            )
        )

        if actual != expected:
            raise ValueError(
                "Test step numbers must "
                "start at 1 and increment "
                "sequentially"
            )

        return self


class AITestCaseGeneration(BaseModel):

    model_config = ConfigDict(
        extra="forbid"
    )

    requirement_id: str = Field(
        min_length=1,
        max_length=100
    )

    scenario_id: str = Field(
        min_length=3,
        max_length=100
    )

    test_cases: list[AITestCase] = Field(
        min_length=1,
        max_length=30
    )


    @field_validator(
        "requirement_id",
        "scenario_id",
        mode="before"
    )
    @classmethod
    def clean_parent_ids(
        cls,
        value
    ):

        if isinstance(value, str):
            return value.strip()

        return value


    @model_validator(
        mode="after"
    )
    def validate_unique_test_case_ids(
        self
    ):

        ids = [
            test_case.test_case_id
            for test_case in self.test_cases
        ]

        if len(ids) != len(set(ids)):
            raise ValueError(
                "AI generated duplicate "
                "test case IDs"
            )

        return self
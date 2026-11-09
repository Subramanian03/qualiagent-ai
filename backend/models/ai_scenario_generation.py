from typing import Literal

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import field_validator
from pydantic import model_validator


AIScenarioType = Literal[
    "functional",
    "negative",
    "boundary",
    "validation",
    "integration",
    "security",
    "performance",
    "accessibility",
]


AIScenarioPriority = Literal[
    "low",
    "medium",
    "high",
    "critical",
]


class AIScenario(BaseModel):

    model_config = ConfigDict(
        extra="forbid"
    )

    scenario_id: str = Field(
        min_length=3,
        max_length=100
    )

    title: str = Field(
        min_length=3,
        max_length=255
    )

    description: str = Field(
        min_length=10,
        max_length=5000
    )

    scenario_type: AIScenarioType

    priority: AIScenarioPriority


    @field_validator(
        "scenario_id",
        "title",
        "description",
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
        "scenario_type",
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


class AIScenarioGeneration(BaseModel):

    model_config = ConfigDict(
        extra="forbid"
    )

    requirement_id: str = Field(
        min_length=1,
        max_length=100
    )

    scenarios: list[AIScenario] = Field(
        min_length=1,
        max_length=20
    )


    @field_validator(
        "requirement_id",
        mode="before"
    )
    @classmethod
    def clean_requirement_id(
        cls,
        value
    ):

        if isinstance(value, str):
            return value.strip()

        return value


    @model_validator(
        mode="after"
    )
    def validate_unique_scenario_ids(
        self
    ):

        scenario_ids = [
            scenario.scenario_id
            for scenario in self.scenarios
        ]

        if (
            len(scenario_ids) !=
            len(set(scenario_ids))
        ):
            raise ValueError(
                "AI generated duplicate "
                "scenario IDs"
            )

        return self
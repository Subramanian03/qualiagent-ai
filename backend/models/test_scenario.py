from datetime import datetime
from typing import Literal

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


ScenarioType = Literal[
    "functional",
    "negative",
    "boundary",
    "validation",
    "integration",
    "security",
    "performance",
    "accessibility"
]


ScenarioPriority = Literal[
    "low",
    "medium",
    "high",
    "critical"
]


ScenarioSource = Literal[
    "ai",
    "manual",
    "legacy"
]


class TestScenarioCreate(BaseModel):

    scenario_id: str = Field(
        min_length=1,
        max_length=100
    )

    title: str = Field(
        min_length=3,
        max_length=255
    )

    description: str | None = Field(
        default=None,
        max_length=5000
    )

    scenario_type: ScenarioType = (
        "functional"
    )

    priority: ScenarioPriority = (
        "medium"
    )

    source: ScenarioSource = "manual"


class TestScenarioResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    requirement_db_id: int

    scenario_id: str
    title: str
    description: str | None

    scenario_type: ScenarioType
    priority: ScenarioPriority
    source: ScenarioSource

    created_at: datetime
    updated_at: datetime
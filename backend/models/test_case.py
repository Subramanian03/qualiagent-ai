from datetime import datetime
from pydantic import field_validator
from typing import Literal

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

from backend.models.requirement import RequirementInput


class TestStep(BaseModel):
    step_number: int = Field(
        ge=1
    )

    action: str = Field(
        min_length=1
    )

    expected_result: str = Field(
        min_length=1
    )


class TestCase(BaseModel):
    test_case_id: str
    requirement_id: str
    title: str

    test_type: Literal[
        "positive",
        "negative",
        "boundary",
        "security",
        "usability"
    ]

    priority: Literal[
        "low",
        "medium",
        "high",
        "critical"
    ]

    preconditions: list[str]

    test_data: list[str]

    steps: list[TestStep]

    automation_candidate: bool


class TestCaseGenerationRequest(BaseModel):
    requirement: RequirementInput


class TestCaseGenerationResponse(BaseModel):
    requirement_id: str
    total_test_cases: int
    test_cases: list[TestCase]


class PersistedTestCaseResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    test_case_id: str
    requirement_db_id: int
    test_scenario_db_id: int | None = None
    requirement_id: str
    title: str
    test_type: str
    priority: str
    preconditions: list[str]
    test_data: list[str]
    steps: list[TestStep]
    automation_candidate: bool
    execution_type: Literal[
        "manual",
        "automation",
        "both"
    ]
    review_status: str
    created_at: datetime

class TestCaseStatusUpdate(BaseModel):
    review_status: Literal[
        "draft",
        "approved",
        "rejected"
    ]

class TestCaseExecutionTypeUpdate(
    BaseModel
):

    execution_type: Literal[
        "manual",
        "automation",
        "both"
    ]
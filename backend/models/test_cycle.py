from datetime import datetime
from typing import Literal

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import model_validator


class CycleTestItemCreate(
    BaseModel
):

    model_config = ConfigDict(
        extra="forbid"
    )


    test_case_id: int = Field(
        ge=1
    )


    execution_mode: Literal[
        "manual",
        "automation"
    ]


class TestCycleCreate(
    BaseModel
):

    model_config = ConfigDict(
        extra="forbid"
    )


    name: str = Field(
        min_length=3,
        max_length=200
    )


    release: str | None = Field(
        default=None,
        max_length=100
    )


    environment: str | None = Field(
        default=None,
        max_length=100
    )


    items: list[
        CycleTestItemCreate
    ] = Field(
        min_length=1
    )


    @model_validator(
        mode="after"
    )
    def validate_unique_test_cases(
        self
    ):

        test_case_ids = [
            item.test_case_id
            for item in self.items
        ]


        if (
            len(test_case_ids) !=
            len(set(test_case_ids))
        ):

            raise ValueError(
                "A Test Case can only be "
                "added once to a Test Cycle"
            )


        return self


class FrozenAutomationResponse(
    BaseModel
):

    model_config = ConfigDict(
        from_attributes=True
    )


    id: int

    version: int

    engine: str

    language: str


class CycleTestItemResponse(
    BaseModel
):

    model_config = ConfigDict(
        from_attributes=True
    )


    id: int

    cycle_id: int

    test_case_id: int

    test_case_key: str

    test_case_title: str

    execution_mode: Literal[
        "manual",
        "automation"
    ]

    automation_version_id: (
        int | None
    )

    automation_version_number: (
        int | None
    )

    automation_engine: (
        str | None
    )

    automation_language: (
        str | None
    )

    execution_id: (
        int | None
    )

    status: Literal[
        "not_run",
        "running",
        "passed",
        "failed",
        "blocked",
        "skipped",
        "error",
    ]

    position: int

    actual_result: str | None

    comment: str | None

    defect_reference: str | None

    created_at: datetime

    updated_at: datetime | None

class TestCycleResultSummary(
    BaseModel
):

    total: int

    completed: int

    not_run: int

    running: int

    passed: int

    failed: int

    blocked: int

    skipped: int

    error: int

    completion_eligible: bool

class TestCycleResponse(
    BaseModel
):

    model_config = ConfigDict(
        from_attributes=True
    )


    id: int

    project_id: int

    name: str

    release: str | None

    environment: str | None

    status: Literal[
        "draft",
        "ready",
        "in_progress",
        "completed",
        "cancelled"
    ]

    created_at: datetime

    started_at: datetime | None

    completed_at: datetime | None

    items: list[
        CycleTestItemResponse
    ]


class TestCycleListItem(
    BaseModel
):

    model_config = ConfigDict(
        from_attributes=True
    )


    id: int

    project_id: int

    name: str

    release: str | None

    environment: str | None

    status: str

    created_at: datetime

class TestCycleStatusUpdate(
    BaseModel
):

    model_config = ConfigDict(
        extra="forbid"
    )


    status: Literal[
        "ready",
        "in_progress",
        "completed",
        "cancelled",
    ]


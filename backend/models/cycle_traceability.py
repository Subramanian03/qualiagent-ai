from datetime import datetime

from pydantic import BaseModel


class CycleTraceabilityExecution(
    BaseModel
):

    id: int

    status: str

    exit_code: int | None

    duration_ms: int | None

    screenshot_available: bool

    trace_available: bool


class CycleTraceabilityOccurrence(
    BaseModel
):

    cycle_id: int

    cycle_name: str

    cycle_status: str

    release: str | None

    environment: str | None

    cycle_item_id: int

    position: int

    execution_mode: str

    result_status: str

    actual_result: str | None

    comment: str | None

    defect_reference: str | None

    automation_version_id: int | None

    automation_version_number: int | None

    automation_engine: str | None

    automation_language: str | None

    execution: (
        CycleTraceabilityExecution |
        None
    )

    cycle_started_at: datetime | None

    cycle_completed_at: datetime | None


class CycleTraceabilityTestCase(
    BaseModel
):

    id: int

    test_case_id: str

    title: str

    test_type: str | None

    priority: str | None

    current_execution_type: str | None

    occurrences: list[
        CycleTraceabilityOccurrence
    ]


class CycleTraceabilityScenario(
    BaseModel
):

    id: int

    scenario_id: str

    title: str

    test_cases: list[
        CycleTraceabilityTestCase
    ]


class CycleTraceabilityRequirement(
    BaseModel
):

    id: int

    requirement_id: str

    title: str

    scenarios: list[
        CycleTraceabilityScenario
    ]


class ProjectCycleTraceability(
    BaseModel
):

    project_id: int

    project_name: str

    requirements: list[
        CycleTraceabilityRequirement
    ]
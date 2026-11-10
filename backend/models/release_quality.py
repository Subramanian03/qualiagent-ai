from typing import Literal

from pydantic import BaseModel


ReleaseReadinessSignal = Literal[
    "ready",
    "at_risk",
    "not_ready",
]

ReleaseRiskSeverity = Literal[
    "blocker",
    "high",
]


class ReleaseExecutionSummary(
    BaseModel
):

    cycles: int

    completed_cycles: int

    planned_tests: int

    completed_tests: int

    not_run: int

    running: int

    passed: int

    failed: int

    blocked: int

    skipped: int

    error: int

    pass_rate: float


class ReleaseExecutionModeSummary(
    BaseModel
):

    manual_total: int

    manual_passed: int

    manual_failed: int

    manual_blocked: int

    manual_skipped: int

    automation_total: int

    automation_passed: int

    automation_failed: int

    automation_error: int


class ReleaseEvidenceSummary(
    BaseModel
):

    executions: int

    screenshots: int

    traces: int


class ReleaseReadinessReason(
    BaseModel
):

    code: str

    message: str

class ReleaseRiskExecution(
    BaseModel
):

    id: int

    status: str

    exit_code: int | None

    duration_ms: int | None

    screenshot_available: bool

    trace_available: bool

class ReleaseRiskItem(
    BaseModel
):

    severity: ReleaseRiskSeverity

    risk_code: str

    requirement_id: str

    requirement_title: str

    scenario_id: str

    scenario_title: str

    test_case_db_id: int

    test_case_id: str

    test_case_title: str

    cycle_id: int

    cycle_name: str

    cycle_status: str

    release: str | None

    environment: str | None

    execution_mode: str

    result_status: str

    automation_version_id: int | None

    automation_version_number: int | None

    automation_engine: str | None

    automation_language: str | None

    execution: ReleaseRiskExecution | None

class ProjectReleaseQuality(
    BaseModel
):

    project_id: int

    release: str

    environment: str | None

    signal: ReleaseReadinessSignal

    execution: ReleaseExecutionSummary

    execution_modes: (
        ReleaseExecutionModeSummary
    )

    evidence: ReleaseEvidenceSummary

    reasons: list[
        ReleaseReadinessReason
    ]
    risks: list[
        ReleaseRiskItem
    ]
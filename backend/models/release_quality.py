from typing import Literal

from pydantic import BaseModel


ReleaseReadinessSignal = Literal[
    "ready",
    "at_risk",
    "not_ready",
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
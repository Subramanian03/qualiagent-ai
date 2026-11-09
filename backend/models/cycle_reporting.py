from pydantic import BaseModel


class CycleStatusSummary(
    BaseModel
):

    total: int

    draft: int

    ready: int

    in_progress: int

    completed: int


class CycleResultSummary(
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

    pass_rate: float


class ManualResultSummary(
    BaseModel
):

    total: int

    passed: int

    failed: int

    blocked: int

    skipped: int


class AutomationResultSummary(
    BaseModel
):

    total: int

    passed: int

    failed: int

    error: int


class ExecutionEvidenceSummary(
    BaseModel
):

    executions: int

    screenshots: int

    traces: int

class CycleReportingFilterOptions(
    BaseModel
):

    releases: list[str]

    environments: list[str]

    cycle_statuses: list[str]

    result_statuses: list[str]

    execution_modes: list[str]

class ProjectCycleQualitySummary(
    BaseModel
):

    project_id: int

    filter_options: (
        CycleReportingFilterOptions
    )

    cycles: CycleStatusSummary

    results: CycleResultSummary

    manual: ManualResultSummary

    automation: AutomationResultSummary

    evidence: ExecutionEvidenceSummary
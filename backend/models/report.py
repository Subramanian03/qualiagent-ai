from pydantic import BaseModel


class ProjectQualitySummary(BaseModel):

    project_id: int
    project_name: str

    requirements: int

    test_cases: int
    draft_tests: int
    approved_tests: int
    rejected_tests: int

    automation_candidates: int
    automation_ready: int

    executions: int
    passed: int
    failed: int
    errors: int

    pass_rate: float

class RequirementCoverage(BaseModel):

    requirement_db_id: int
    requirement_id: str
    title: str

    test_cases: int
    approved_tests: int

    automation_ready: int

    executions: int

    latest_execution_id: int | None
    latest_status: str | None
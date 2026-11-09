from datetime import datetime
from typing import Literal

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import SecretStr


ExecutionStatus = Literal[
    "pending",
    "running",
    "passed",
    "failed",
    "error"
]


class ExecutionCreate(BaseModel):

    automation_script_id: int

class ExecutionRunRequest(BaseModel):

    test_password: SecretStr | None = None


class ExecutionResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    automation_script_id: int
    status: ExecutionStatus

    started_at: datetime | None
    completed_at: datetime | None

    duration_ms: int | None
    exit_code: int | None

    stdout: str | None
    stderr: str | None
    error_message: str | None

    screenshot_path: str | None
    trace_path: str | None

    created_at: datetime

class ProjectExecutionResponse(
    ExecutionResponse
):

    test_case_db_id: int
    test_case_id: str
    test_case_title: str
    requirement_id: str

    framework: str
    language: str

    
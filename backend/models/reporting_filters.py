
from typing import Literal

from pydantic import BaseModel


CycleStatusFilter = Literal[
    "draft",
    "ready",
    "in_progress",
    "completed",
]


CycleResultFilter = Literal[
    "not_run",
    "running",
    "passed",
    "failed",
    "blocked",
    "skipped",
    "error",
]


ExecutionModeFilter = Literal[
    "manual",
    "automation",
]


class CycleReportingFilters(
    BaseModel
):

    release: str | None = None

    environment: str | None = None

    cycle_status: (
        CycleStatusFilter |
        None
    ) = None

    result_status: (
        CycleResultFilter |
        None
    ) = None

    execution_mode: (
        ExecutionModeFilter |
        None
    ) = None
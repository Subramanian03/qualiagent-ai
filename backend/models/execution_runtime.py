from pydantic import BaseModel
from pydantic import ConfigDict

from backend.models.automation_runtime_input import (
    AutomationRuntimeInputSubmission,
)


class ExecutionRuntimeRequest(
    AutomationRuntimeInputSubmission
):

    model_config = ConfigDict(
        extra="forbid"
    )
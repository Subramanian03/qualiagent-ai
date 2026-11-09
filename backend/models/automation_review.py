from typing import Literal

from pydantic import BaseModel
from pydantic import ConfigDict


AutomationReviewStatus = Literal[
    "ready",
    "rejected",
]


class AutomationReviewRequest(
    BaseModel
):

    model_config = ConfigDict(
        extra="forbid"
    )

    status: AutomationReviewStatus
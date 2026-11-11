from pydantic import BaseModel
from pydantic import Field

from backend.models.failure_analysis import (
    FailureClassification,
    FailureRecommendationType,
)


class FailureAnalysisAIOutput(
    BaseModel
):

    classification: (
        FailureClassification
    )

    confidence: float = Field(
        ge=0.0,
        le=1.0
    )

    summary: str = Field(
        min_length=1,
        max_length=2000
    )

    evidence: list[str] = Field(
        min_length=1,
        max_length=12
    )

    likely_cause: str = Field(
        min_length=1,
        max_length=3000
    )

    recommendation_type: (
        FailureRecommendationType
    )

    recommended_action: str = Field(
        min_length=1,
        max_length=3000
    )

    suggested_change_applicable: bool

    suggested_change_rationale: str = Field(
        min_length=1,
        max_length=3000
    )

    current_code_excerpt: str | None = Field(
        default=None,
        max_length=6000
    )

    suggested_code_excerpt: str | None = Field(
        default=None,
        max_length=6000
    )

    full_replacement_code: str | None = Field(
        default=None,
        max_length=20000
    )
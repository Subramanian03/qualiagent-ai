from typing import Literal

from pydantic import BaseModel
from pydantic import Field
from pydantic import Field


FailureClassification = Literal[
    "product_failure",
    "automation_failure",
    "test_data_failure",
    "environment_failure",
    "unknown",
]


FailureAnalysisStatus = Literal[
    "draft",
    "reviewed",
]


FailureRecommendationType = Literal[
    "investigate_product",
    "update_automation",
    "update_test_data",
    "investigate_environment",
    "manual_investigation",
]


class FailureEvidenceSummary(
    BaseModel
):

    execution_id: int

    execution_status: str

    exit_code: int | None

    duration_ms: int | None

    screenshot_available: bool

    trace_available: bool

    error_excerpt: str | None

    output_excerpt: str | None

class FailureTestContext(
    BaseModel
):

    project_id: int

    project_name: str

    requirement_id: str

    requirement_title: str

    scenario_id: str

    scenario_title: str

    test_case_db_id: int

    test_case_id: str

    test_case_title: str

    test_case_type: str | None

    test_case_priority: str | None


class FailureAutomationContext(
    BaseModel
):

    automation_version_id: int

    version_number: int

    framework: str | None

    engine: str | None

    language: str | None

    status: str

    source: str | None

    parent_version_id: int | None

    code_excerpt: str | None


class FailureEvidencePackage(
    BaseModel
):

    execution_id: int

    execution_status: str

    exit_code: int | None

    duration_ms: int | None

    screenshot_available: bool

    trace_available: bool

    error_excerpt: str | None

    output_excerpt: str | None

    test_context: FailureTestContext

    automation_context: (
        FailureAutomationContext |
        None
    )

    redaction_applied: bool

    redaction_count: int

    evidence_paths_exposed: bool = False

    runtime_secrets_included: bool = False

class FailureAnalysisFinding(
    BaseModel
):

    classification: FailureClassification

    confidence: float = Field(
        ge=0.0,
        le=1.0
    )

    summary: str

    evidence: list[str]

    likely_cause: str

    recommendation_type: (
        FailureRecommendationType
    )

    recommended_action: str


class SuggestedAutomationChange(
    BaseModel
):

    applicable: bool

    rationale: str

    current_code_excerpt: str | None = None

    suggested_code_excerpt: str | None = None

    full_replacement_code: str | None = None

class FailureAnalysisProviderMetadata(
    BaseModel
):

    provider: str

    model: str | None

    mode: str

    raw_response_stored: bool = False



class FailureAnalysisResponse(
    BaseModel
):

    execution_id: int

    automation_version_id: int | None

    analysis_status: (
        FailureAnalysisStatus
    )

    evidence: FailureEvidenceSummary

    finding: FailureAnalysisFinding

    suggested_automation_change: (
        SuggestedAutomationChange |
        None
    )

    human_review_required: bool = True

    execution_result_changed: bool = False

    automation_changed: bool = False

    provider: (
        FailureAnalysisProviderMetadata
    )

class CreateFailureSuggestionDraftRequest(
    BaseModel
):

    source_execution_id: int

    parent_automation_version_id: int

    code: str = Field(
        min_length=1,
        max_length=100000
    )

    rationale: str = Field(
        min_length=1,
        max_length=5000
    )

    classification: (
        FailureClassification
    )

    recommendation_type: (
        FailureRecommendationType
    )


class CreateFailureSuggestionDraftResponse(
    BaseModel
):

    source_execution_id: int

    parent_automation_version_id: int

    created_automation_version_id: int

    created_version_number: int

    status: str

    human_review_required: bool = True

    source_execution_changed: bool = False

    parent_automation_changed: bool = False
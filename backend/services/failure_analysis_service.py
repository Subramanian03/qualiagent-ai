from sqlalchemy.orm import Session

from backend.ai.factory import (
    get_ai_provider,
)

from backend.ai.settings import (
    load_ai_settings,
)

from backend.models.failure_analysis import (
    FailureAnalysisFinding,
    FailureAnalysisProviderMetadata,
    FailureAnalysisResponse,
    FailureEvidenceSummary,
    SuggestedAutomationChange,
)

from backend.services.failure_analysis_parser import (
    parse_failure_analysis_output,
)

from backend.services.failure_analysis_prompt_service import (
    SYSTEM_PROMPT,
    build_failure_analysis_prompt,
)

from backend.services.failure_evidence_service import (
    collect_failure_evidence,
)


def create_failure_analysis_response(
    *,
    evidence,
    ai_output,
    provider_name: str,
    model_name: str | None,
    provider_mode: str
) -> FailureAnalysisResponse:

    automation_version_id = None


    if (
        evidence.automation_context
        is not None
    ):

        automation_version_id = (
            evidence
            .automation_context
            .automation_version_id
        )


    suggested_change = (
        SuggestedAutomationChange(
            applicable=(
                ai_output
                .suggested_change_applicable
            ),

            rationale=(
                ai_output
                .suggested_change_rationale
            ),

            current_code_excerpt=(
                ai_output
                .current_code_excerpt
            ),

            suggested_code_excerpt=(
                ai_output
                .suggested_code_excerpt
            ),

            full_replacement_code=(
                ai_output
                .full_replacement_code
            )
        )
    )


    return FailureAnalysisResponse(
        execution_id=(
            evidence.execution_id
        ),

        automation_version_id=(
            automation_version_id
        ),

        analysis_status="draft",

        evidence=FailureEvidenceSummary(
            execution_id=(
                evidence.execution_id
            ),

            execution_status=(
                evidence.execution_status
            ),

            exit_code=(
                evidence.exit_code
            ),

            duration_ms=(
                evidence.duration_ms
            ),

            screenshot_available=(
                evidence
                .screenshot_available
            ),

            trace_available=(
                evidence
                .trace_available
            ),

            error_excerpt=(
                evidence.error_excerpt
            ),

            output_excerpt=(
                evidence.output_excerpt
            )
        ),

        finding=FailureAnalysisFinding(
            classification=(
                ai_output.classification
            ),

            confidence=(
                ai_output.confidence
            ),

            summary=(
                ai_output.summary
            ),

            evidence=(
                ai_output.evidence
            ),

            likely_cause=(
                ai_output.likely_cause
            ),

            recommendation_type=(
                ai_output
                .recommendation_type
            ),

            recommended_action=(
                ai_output
                .recommended_action
            )
        ),

        suggested_automation_change=(
            suggested_change
        ),

        human_review_required=True,

        execution_result_changed=False,

        automation_changed=False,

        provider=(
            FailureAnalysisProviderMetadata(
                provider=(
                    provider_name
                ),

                model=(
                    model_name
                ),

                mode=(
                    provider_mode
                ),

                raw_response_stored=False
            )
        )
    )


def analyze_execution_failure(
    db: Session,
    execution_id: int
) -> FailureAnalysisResponse:

    evidence = (
        collect_failure_evidence(
            db,
            execution_id
        )
    )


    settings = (
        load_ai_settings()
    )


    provider = (
        get_ai_provider()
    )


    user_prompt = (
        build_failure_analysis_prompt(
            evidence
        )
    )


    raw_result = (
        provider.generate(
            system_prompt=(
                SYSTEM_PROMPT
            ),

            user_prompt=(
                user_prompt
            ),

            task=(
                "failure_analysis"
            )
        )
    )


    ai_output = (
        parse_failure_analysis_output(
            raw_result
        )
    )


    return (
        create_failure_analysis_response(
            evidence=(
                evidence
            ),

            ai_output=(
                ai_output
            ),

            provider_name=(
                settings.provider
            ),

            model_name=(
                settings.model
            ),

            provider_mode=(
                settings.mode
            )
        )
    )
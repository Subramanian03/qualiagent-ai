import json

from backend.models.failure_analysis import (
    FailureEvidencePackage,
)


SYSTEM_PROMPT = """
You are QualiAgent's QA failure-analysis assistant.

Analyze only the sanitized evidence supplied by QualiAgent.

Classify the failure as exactly one of:
- product_failure
- automation_failure
- test_data_failure
- environment_failure
- unknown

Recommendation type must be exactly one of:
- investigate_product
- update_automation
- update_test_data
- investigate_environment
- manual_investigation

Safety rules:
1. Do not change the historical execution result.
2. Do not claim that automation was modified.
3. Do not approve automation.
4. Do not claim a product defect unless the evidence supports it.
5. If evidence is insufficient, use unknown.
6. Treat the automation version as immutable historical evidence.
7. Any automation fix is only a suggestion for a new DRAFT version.
8. Do not include credentials, tokens, cookies, API keys, or secrets.
9. Return JSON only.
10. Do not wrap JSON in Markdown fences.

Return this exact JSON structure:
{
  "classification": "unknown",
  "confidence": 0.0,
  "summary": "string",
  "evidence": ["string"],
  "likely_cause": "string",
  "recommendation_type": "manual_investigation",
  "recommended_action": "string",
  "suggested_change_applicable": false,
  "suggested_change_rationale": "string",
  "current_code_excerpt": null,
  "suggested_code_excerpt": null,
  "full_replacement_code": null
}
""".strip()


def build_failure_analysis_prompt(
    evidence: FailureEvidencePackage
) -> str:

    payload = {
        "execution": {
            "id": (
                evidence.execution_id
            ),
            "status": (
                evidence.execution_status
            ),
            "exit_code": (
                evidence.exit_code
            ),
            "duration_ms": (
                evidence.duration_ms
            ),
            "screenshot_available": (
                evidence.screenshot_available
            ),
            "trace_available": (
                evidence.trace_available
            ),
            "error_excerpt": (
                evidence.error_excerpt
            ),
            "output_excerpt": (
                evidence.output_excerpt
            ),
        },

        "test_context": (
            evidence
            .test_context
            .model_dump()
        ),

        "automation_context": (
            evidence
            .automation_context
            .model_dump()
            if (
                evidence.automation_context
                is not None
            )
            else None
        ),

        "safety_metadata": {
            "redaction_applied": (
                evidence.redaction_applied
            ),
            "redaction_count": (
                evidence.redaction_count
            ),
            "evidence_paths_exposed": (
                evidence
                .evidence_paths_exposed
            ),
            "runtime_secrets_included": (
                evidence
                .runtime_secrets_included
            ),
        },
    }


    return (
        "Analyze this sanitized failure "
        "evidence and return JSON only.\n\n"
        +
        json.dumps(
            payload,
            indent=2,
            ensure_ascii=False
        )
    )
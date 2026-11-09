import json

from pydantic import ValidationError

from backend.ai.errors import (
    AIProviderResponseError,
)
from backend.ai.factory import (
    get_ai_provider,
)
from backend.models.ai_requirement_analysis import (
    AIRequirementAnalysis,
)


REQUIREMENT_ANALYSIS_SYSTEM_PROMPT = """
You are QualiAgent's senior software QA
requirement analyst.

Analyse one software requirement or user
story.

Your analysis must be grounded only in the
requirement supplied by the user.

Do not invent application behaviour,
screens, fields, APIs, business rules,
credentials, selectors, or integrations
that are not present in the requirement.

When information required for reliable
testing is missing, add a clarification
question instead of making an assumption.

Evaluate whether the requirement is
testable. Identify its QA risk, important
keywords, relevant test categories,
acceptance criteria, and clarification
questions.

Return exactly one JSON object with these
fields:

{
  "testable": true,
  "risk_level": "low | medium | high | critical",
  "application_type": "web | mobile | api | desktop | other",
  "summary": "string",
  "identified_keywords": ["string"],
  "suggested_test_types": [
    "positive | negative | boundary |
     validation | functional | integration |
     security | performance | accessibility |
     usability | compatibility"
  ],
  "acceptance_criteria": ["string"],
  "questions": ["string"]
}

Rules:

1. risk_level must be one of:
   low, medium, high, critical.

2. application_type must be one of:
   web, mobile, api, desktop, other.

3. suggested_test_types must use only the
   permitted test-type values.

4. Each acceptance criterion must be
   observable and testable.

5. Questions must contain only genuine
   information gaps.

6. Do not include Markdown.

7. Do not return text outside the JSON
   object.
""".strip()


def build_requirement_analysis_prompt(
    requirement
) -> str:

    payload = {
        "requirement_db_id":
            getattr(
                requirement,
                "id",
                None
            ),

        "requirement_id":
            getattr(
                requirement,
                "requirement_id",
                ""
            ),

        "title":
            getattr(
                requirement,
                "title",
                ""
            ),

        "description":
            getattr(
                requirement,
                "description",
                ""
            ),

        "application_type":
            getattr(
                requirement,
                "application_type",
                "other"
            ),
    }

    return (
        "Analyse the following QualiAgent "
        "requirement:\n\n"
        + json.dumps(
            payload,
            ensure_ascii=False,
            indent=2
        )
    )


def analyse_requirement_with_ai(
    requirement
) -> AIRequirementAnalysis:

    provider = get_ai_provider()

    raw_result = provider.generate(
        system_prompt=(
            REQUIREMENT_ANALYSIS_SYSTEM_PROMPT
        ),
        user_prompt=(
            build_requirement_analysis_prompt(
                requirement
            )
        ),
        task="requirement_analysis"
    )

    try:

        return (
            AIRequirementAnalysis
            .model_validate(
                raw_result
            )
        )

    except ValidationError as exc:

        raise AIProviderResponseError(
            "AI requirement analysis did "
            "not match the required schema: "
            f"{exc}"
        ) from exc
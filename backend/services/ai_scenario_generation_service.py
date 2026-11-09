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

from backend.models.ai_scenario_generation import (
    AIScenarioGeneration,
)


SCENARIO_GENERATION_SYSTEM_PROMPT = """
You are QualiAgent's senior software QA
test designer.

Your task is to generate high-quality test
scenarios for exactly one software
requirement or user story.

Generate scenarios only from the supplied
requirement and its validated QA analysis.

Do not invent screens, fields, selectors,
APIs, credentials, business rules,
integrations, workflows, thresholds,
messages, or behaviours that are not
supported by the requirement.

If the requirement does not provide enough
information for a particular scenario, do
not invent the missing behaviour.

Generate scenarios at the scenario level,
not detailed test cases.

A scenario represents a meaningful testing
objective. Detailed steps and test data
belong to Test Cases and will be generated
later.

Cover the relevant testing perspectives
based on the actual requirement. Examples
may include:

- functional
- negative
- boundary
- validation
- integration
- security
- performance
- accessibility

Only include a perspective when it is
meaningful for the supplied requirement.

Return exactly one JSON object using this
structure:

{
  "requirement_id": "REQ-001",
  "scenarios": [
    {
      "scenario_id": "REQ-001-SCN-001",
      "title": "Scenario title",
      "description": "Observable scenario objective",
      "scenario_type": "functional",
      "priority": "high"
    }
  ]
}

Allowed scenario_type values:

functional
negative
boundary
validation
integration
security
performance
accessibility

Allowed priority values:

low
medium
high
critical

Rules:

1. Generate between 1 and 20 scenarios.

2. Every scenario must map directly to the
   supplied requirement.

3. Do not generate duplicate scenarios.

4. scenario_id must use this pattern:

   <requirement_id>-SCN-XXX

   Example:

   REQ-LOGIN-001-SCN-001

5. Scenario numbering must begin at 001 and
   increment sequentially.

6. The returned requirement_id must exactly
   match the supplied requirement_id.

7. Scenario descriptions must state what
   behaviour or quality condition should be
   verified, not implementation details.

8. Do not generate test steps.

9. Do not generate automation selectors.

10. Do not generate automation code.

11. Do not include Markdown.

12. Do not return any text outside the JSON
    object.
""".strip()


def build_scenario_generation_prompt(
    requirement,
    analysis: AIRequirementAnalysis
) -> str:

    requirement_payload = {
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


    payload = {
        "requirement":
            requirement_payload,

        "validated_analysis":
            analysis.model_dump(),
    }


    return (
        "Generate test scenarios for this "
        "QualiAgent requirement.\n\n"
        + json.dumps(
            payload,
            ensure_ascii=False,
            indent=2
        )
    )


def generate_scenarios_with_ai(
    requirement,
    analysis: AIRequirementAnalysis
) -> AIScenarioGeneration:

    provider = get_ai_provider()

    raw_result = provider.generate(
        system_prompt=(
            SCENARIO_GENERATION_SYSTEM_PROMPT
        ),
        user_prompt=(
            build_scenario_generation_prompt(
                requirement,
                analysis
            )
        ),
        task="scenario_generation"
    )


    try:

        validated = (
            AIScenarioGeneration
            .model_validate(
                raw_result
            )
        )

    except ValidationError as exc:

        raise AIProviderResponseError(
            "AI scenario generation did "
            "not match the required schema: "
            f"{exc}"
        ) from exc


    expected_requirement_id = str(
        getattr(
            requirement,
            "requirement_id",
            ""
        )
    ).strip()


    if (
        validated.requirement_id !=
        expected_requirement_id
    ):
        raise AIProviderResponseError(
            "AI scenario generation returned "
            "a different requirement_id"
        )


    expected_prefix = (
        f"{expected_requirement_id}"
        "-SCN-"
    )


    for index, scenario in enumerate(
        validated.scenarios,
        start=1
    ):

        expected_scenario_id = (
            f"{expected_prefix}"
            f"{index:03d}"
        )

        if (
            scenario.scenario_id !=
            expected_scenario_id
        ):
            raise AIProviderResponseError(
                "AI scenario IDs must be "
                "sequential. Expected "
                f"'{expected_scenario_id}' "
                "but received "
                f"'{scenario.scenario_id}'"
            )


    return validated
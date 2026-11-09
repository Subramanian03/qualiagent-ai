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

from backend.models.ai_test_case_generation import (
    AITestCaseGeneration,
)


TEST_CASE_GENERATION_SYSTEM_PROMPT = """
You are QualiAgent's senior software QA
test-case designer.

Generate detailed test cases for exactly
one supplied test scenario.

Use only:

1. The supplied software requirement.
2. The selected test scenario.
3. The validated requirement analysis.

Do not generate test cases for other
scenarios.

Do not invent application screens, field
names, UI selectors, API paths, database
tables, credentials, error messages,
business rules, thresholds, integrations,
or workflows that are not supported by
the supplied information.

If concrete test-data values are not
provided, describe the required test-data
category instead of inventing a value.

Examples:

Correct:
"Registered user identifier"
"Valid password"
"An invalid authentication credential"

Incorrect:
"standard_user"
"secret_sauce"
"#login-button"

Each test case must be independently
understandable and traceable to the
selected scenario.

Return exactly one JSON object with this
structure:

{
  "requirement_id": "REQ-001",
  "scenario_id": "REQ-001-SCN-001",
  "test_cases": [
    {
      "test_case_id":
        "REQ-001-SCN-001-TC-001",
      "title": "Test case title",
      "test_type": "positive",
      "priority": "high",
      "preconditions": [
        "Precondition"
      ],
      "test_data": [
        "Required test data description"
      ],
      "steps": [
        {
          "step_number": 1,
          "action": "User or system action",
          "expected_result":
            "Observable expected result"
        }
      ],
      "automation_candidate": true
    }
  ]
}

Allowed test_type values:

positive
negative
boundary
validation
functional
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

1. Generate between 1 and 30 test cases.

2. Every test case must map directly to
   the selected scenario.

3. Do not duplicate testing objectives.

4. test_case_id must use this exact
   pattern:

   <scenario_id>-TC-XXX

   Example:

   REQ-001-SCN-001-TC-001

5. Test-case numbering must start at 001
   and increment sequentially.

6. The returned requirement_id must
   exactly match the supplied
   requirement_id.

7. The returned scenario_id must exactly
   match the supplied scenario_id.

8. Step numbering must begin at 1 and
   increment sequentially within each
   test case.

9. Every step must contain both:
   action
   expected_result

10. Expected results must be observable
    and testable.

11. Preconditions must describe only
    required initial conditions.

12. test_data must describe what data is
    required, not fabricate actual
    usernames, passwords, tokens, personal
    data, or production data.

13. Set automation_candidate to true only
    when the test can reasonably be
    automated using deterministic actions
    and assertions.

14. Do not create Playwright selectors.

15. Do not create automation code.

16. Do not include Markdown.

17. Do not return text outside the JSON
    object.
""".strip()


def build_test_case_generation_prompt(
    requirement,
    scenario,
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


    scenario_payload = {
        "scenario_db_id":
            getattr(
                scenario,
                "id",
                None
            ),

        "scenario_id":
            getattr(
                scenario,
                "scenario_id",
                ""
            ),

        "title":
            getattr(
                scenario,
                "title",
                ""
            ),

        "description":
            getattr(
                scenario,
                "description",
                ""
            ),

        "scenario_type":
            getattr(
                scenario,
                "scenario_type",
                "functional"
            ),

        "priority":
            getattr(
                scenario,
                "priority",
                "medium"
            ),
    }


    payload = {
        "requirement":
            requirement_payload,

        "selected_scenario":
            scenario_payload,

        "validated_requirement_analysis":
            analysis.model_dump(),
    }


    return (
        "Generate detailed test cases for "
        "the selected QualiAgent test "
        "scenario.\n\n"
        + json.dumps(
            payload,
            ensure_ascii=False,
            indent=2
        )
    )


def generate_test_cases_with_ai(
    requirement,
    scenario,
    analysis: AIRequirementAnalysis
) -> AITestCaseGeneration:

    provider = get_ai_provider()


    raw_result = provider.generate(
        system_prompt=(
            TEST_CASE_GENERATION_SYSTEM_PROMPT
        ),

        user_prompt=(
            build_test_case_generation_prompt(
                requirement,
                scenario,
                analysis
            )
        ),

        task="test_case_generation"
    )


    try:

        validated = (
            AITestCaseGeneration
            .model_validate(
                raw_result
            )
        )

    except ValidationError as exc:

        raise AIProviderResponseError(
            "AI test-case generation did "
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
            "AI test-case generation "
            "returned a different "
            "requirement_id"
        )


    expected_scenario_id = str(
        getattr(
            scenario,
            "scenario_id",
            ""
        )
    ).strip()


    if (
        validated.scenario_id !=
        expected_scenario_id
    ):

        raise AIProviderResponseError(
            "AI test-case generation "
            "returned a different "
            "scenario_id"
        )


    expected_prefix = (
        f"{expected_scenario_id}"
        "-TC-"
    )


    for index, test_case in enumerate(
        validated.test_cases,
        start=1
    ):

        expected_test_case_id = (
            f"{expected_prefix}"
            f"{index:03d}"
        )


        if (
            test_case.test_case_id !=
            expected_test_case_id
        ):

            raise AIProviderResponseError(
                "AI test-case IDs must be "
                "sequential. Expected "
                f"'{expected_test_case_id}' "
                "but received "
                f"'{test_case.test_case_id}'"
            )


    return validated
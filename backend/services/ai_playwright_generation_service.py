import json
import re

from pydantic import ValidationError

from backend.ai.errors import (
    AIProviderResponseError,
)

from backend.ai.factory import (
    get_ai_provider,
)

from backend.models.ai_automation_generation import (
    AIAutomationGeneration,
)

from backend.models.automation_input_schema import (
    AutomationInputSchema,
)

from backend.models.automation_runtime_input import (
    ValidatedAutomationRuntimeInputs,
)


PLAYWRIGHT_GENERATION_SYSTEM_PROMPT = """
You are QualiAgent's senior Playwright
automation engineer.

Generate one complete Playwright JavaScript
test for exactly one approved Test Case.

The generated source must use:

const { test, expect } =
  require('@playwright/test');

Generate JavaScript only. Do not generate
TypeScript.

Use runtime inputs only through:

process.env.INPUT_KEY

Examples:

process.env.BASE_URL
process.env.TEST_USERNAME
process.env.TEST_PASSWORD

Never embed actual credentials, passwords,
tokens, API keys, private keys or secret
values in the generated source.

Do not invent runtime input keys. Use only
the supplied allowed input definitions.

Use Playwright user-facing locators when
supported by the supplied information, such
as:

page.getByRole(...)
page.getByLabel(...)
page.getByPlaceholder(...)
page.getByText(...)

Do not invent selectors, labels, placeholder
text, element IDs or CSS classes that are
not grounded in the supplied requirement,
scenario, Test Case or application context.

When reliable selectors cannot be derived
from the supplied information, include a
clear JavaScript comment marking the locator
for human review. Do not pretend an invented
selector is reliable.

The test must:

1. Map directly to the selected Test Case.
2. Use test() from @playwright/test.
3. Use expect() assertions for observable
   expected results.
4. Reference runtime inputs through
   process.env.KEY.
5. Avoid logging secrets.
6. Avoid printing environment variables.
7. Avoid shell commands.
8. Avoid spawning processes.
9. Avoid filesystem operations.
10. Avoid dynamic code execution.
11. Avoid network clients other than
    Playwright browser or request fixtures.
12. Avoid arbitrary package imports.
13. Contain one Playwright test only.

Return exactly one JSON object:

{
  "test_case_id":
    "REQ-001-SCN-001-TC-001",
  "framework":
    "playwright",
  "language":
    "javascript",
  "code":
    "complete Playwright JavaScript",
  "used_inputs": [
    "BASE_URL",
    "TEST_USERNAME",
    "TEST_PASSWORD"
  ]
}

Do not include Markdown fences.

Do not include commentary outside the JSON
object.

Preserve authentication identifier semantics
from the supplied Test Case.

Do not transform username into email, email
into username, or a generic login identifier
into either one unless the supplied context
explicitly establishes that meaning.

Use only the supplied runtime input keys.
""".strip()


FORBIDDEN_CODE_PATTERNS = {
    "child_process": r"\bchild_process\b",
    "process execution": (
        r"\b(?:exec|execSync|spawn|spawnSync)"
        r"\s*\("
    ),
    "dynamic evaluation": (
        r"\b(?:eval|Function)\s*\("
    ),
    "filesystem import": (
        r"""require\s*\(\s*?:fs|fs/promises['"]"""
    ),
    "filesystem modules": (
        r"""from\s+?:fs|fs/promises['"]"""
    ),
    "shell command": (
        r"\b(?:powershell|cmd\.exe|bash|sh)\b"
    ),
}


def build_playwright_generation_prompt(
    project,
    requirement,
    scenario,
    test_case,
    input_schema: AutomationInputSchema,
    runtime_inputs:
        ValidatedAutomationRuntimeInputs
) -> str:

    project_payload = {
        "project_db_id":
            getattr(
                project,
                "id",
                None
            ),

        "name":
            getattr(
                project,
                "name",
                ""
            ),

        "description":
            getattr(
                project,
                "description",
                ""
            ),

        "application_type":
            getattr(
                project,
                "application_type",
                "other"
            ),
    }


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
    }


    test_case_payload = {
        "test_case_db_id":
            getattr(
                test_case,
                "id",
                None
            ),

        "test_case_id":
            getattr(
                test_case,
                "test_case_id",
                ""
            ),

        "title":
            getattr(
                test_case,
                "title",
                ""
            ),

        "test_type":
            getattr(
                test_case,
                "test_type",
                "functional"
            ),

        "priority":
            getattr(
                test_case,
                "priority",
                "medium"
            ),

        "preconditions":
            getattr(
                test_case,
                "preconditions",
                []
            )
            or [],

        "test_data":
            getattr(
                test_case,
                "test_data",
                []
            )
            or [],

        "steps":
            getattr(
                test_case,
                "steps",
                []
            )
            or [],
    }


    input_definitions = [
        {
            "key":
                item.key,

            "label":
                item.label,

            "input_type":
                item.input_type,

            "required":
                item.required,

            "secret":
                item.secret,

            "scope":
                item.scope,

            "description":
                item.description,
        }
        for item in input_schema.inputs
    ]


    payload = {
        "project":
            project_payload,

        "requirement":
            requirement_payload,

        "selected_scenario":
            scenario_payload,

        "approved_test_case":
            test_case_payload,

        "allowed_input_definitions":
            input_definitions,

        # Only non-secret values can be
        # included as generation context.
        "non_secret_runtime_values":
            runtime_inputs
            .non_secret_values,

        # Only secret key names are included.
        # Actual secret values are excluded.
        "secret_input_keys":
            list(
                runtime_inputs
                .secret_values
                .keys()
            ),
    }


    return (
        "Generate a complete Playwright "
        "JavaScript test for this approved "
        "QualiAgent Test Case.\n\n"
        + json.dumps(
            payload,
            ensure_ascii=False,
            indent=2
        )
    )

def generate_playwright_with_ai(
    project,
    requirement,
    scenario,
    test_case,
    input_schema: AutomationInputSchema,
    runtime_inputs:
        ValidatedAutomationRuntimeInputs
) -> AIAutomationGeneration:

    validate_generation_context(
        requirement,
        scenario,
        test_case,
        input_schema
    )


    provider = get_ai_provider()


    raw_result = provider.generate(
        system_prompt=(
            PLAYWRIGHT_GENERATION_SYSTEM_PROMPT
        ),

        user_prompt=(
            build_playwright_generation_prompt(
                project,
                requirement,
                scenario,
                test_case,
                input_schema,
                runtime_inputs
            )
        ),

        task="playwright_generation"
    )


    try:

        generated = (
            AIAutomationGeneration
            .model_validate(
                raw_result
            )
        )

    except ValidationError as exc:

        raise AIProviderResponseError(
            "AI Playwright generation did "
            "not match the required schema: "
            f"{exc}"
        ) from exc


    validate_generated_automation(
        generated=generated,
        test_case=test_case,
        input_schema=input_schema,
        runtime_inputs=runtime_inputs
    )


    return generated


def validate_generation_context(
    requirement,
    scenario,
    test_case,
    input_schema: AutomationInputSchema
):

    review_status = str(
        getattr(
            test_case,
            "review_status",
            ""
        )
    ).strip().lower()


    if review_status != "approved":

        raise AIProviderResponseError(
            "Test Case must be approved "
            "before Playwright generation"
        )


    if not bool(
        getattr(
            test_case,
            "automation_candidate",
            False
        )
    ):

        raise AIProviderResponseError(
            "Test Case is not an automation "
            "candidate"
        )


    requirement_db_id = getattr(
        requirement,
        "id",
        None
    )


    if (
        getattr(
            scenario,
            "requirement_db_id",
            None
        ) != requirement_db_id
    ):

        raise AIProviderResponseError(
            "Scenario does not belong to "
            "the supplied Requirement"
        )


    if (
        getattr(
            test_case,
            "requirement_db_id",
            None
        ) != requirement_db_id
    ):

        raise AIProviderResponseError(
            "Test Case does not belong to "
            "the supplied Requirement"
        )


    if (
        getattr(
            test_case,
            "test_scenario_db_id",
            None
        ) != getattr(
            scenario,
            "id",
            None
        )
    ):

        raise AIProviderResponseError(
            "Test Case does not belong to "
            "the supplied Scenario"
        )


    expected_test_case_id = str(
        getattr(
            test_case,
            "test_case_id",
            ""
        )
    ).strip()


    if (
        input_schema.test_case_id !=
        expected_test_case_id
    ):

        raise AIProviderResponseError(
            "Automation input schema belongs "
            "to a different Test Case"
        )


def validate_generated_automation(
    *,
    generated: AIAutomationGeneration,
    test_case,
    input_schema: AutomationInputSchema,
    runtime_inputs:
        ValidatedAutomationRuntimeInputs
):

    expected_test_case_id = str(
        getattr(
            test_case,
            "test_case_id",
            ""
        )
    ).strip()


    if (
        generated.test_case_id !=
        expected_test_case_id
    ):

        raise AIProviderResponseError(
            "AI automation generation "
            "returned a different "
            "test_case_id"
        )


    allowed_keys = {
        item.key
        for item in input_schema.inputs
    }


    used_keys = set(
        generated.used_inputs
    )


    unexpected_keys = (
        used_keys -
        allowed_keys
    )


    if unexpected_keys:

        raise AIProviderResponseError(
            "Generated automation uses "
            "unapproved input keys: "
            + ", ".join(
                sorted(
                    unexpected_keys
                )
            )
        )


    submitted_keys = (
        set(
            runtime_inputs
            .non_secret_values
            .keys()
        )
        |
        set(
            runtime_inputs
            .secret_values
            .keys()
        )
    )


    missing_submitted_keys = (
        used_keys -
        submitted_keys
    )


    if missing_submitted_keys:

        raise AIProviderResponseError(
            "Generated automation references "
            "runtime inputs that were not "
            "submitted: "
            + ", ".join(
                sorted(
                    missing_submitted_keys
                )
            )
        )


    for key in used_keys:

        expected_reference = (
            f"process.env.{key}"
        )

        if (
            expected_reference not in
            generated.code
        ):

            raise AIProviderResponseError(
                "Generated automation must "
                "reference runtime input "
                f"'{key}' through "
                f"'{expected_reference}'"
            )


    validate_required_input_usage(
        generated,
        input_schema
    )


    reject_secret_literals(
        generated.code,
        runtime_inputs
    )


    reject_forbidden_code(
        generated.code
    )


def validate_required_input_usage(
    generated: AIAutomationGeneration,
    input_schema: AutomationInputSchema
):

    required_keys = {
        item.key
        for item in input_schema.inputs
        if item.required
    }


    used_keys = set(
        generated.used_inputs
    )


    missing_required_keys = (
        required_keys -
        used_keys
    )


    if missing_required_keys:

        raise AIProviderResponseError(
            "Generated automation does not "
            "use required inputs: "
            + ", ".join(
                sorted(
                    missing_required_keys
                )
            )
        )


def reject_secret_literals(
    code: str,
    runtime_inputs:
        ValidatedAutomationRuntimeInputs
):

    for key, secret_value in (
        runtime_inputs
        .secret_values
        .items()
    ):

        if not secret_value:
            continue


        if secret_value in code:

            raise AIProviderResponseError(
                "Generated automation contains "
                "a submitted secret value "
                f"for '{key}'"
            )


def reject_forbidden_code(
    code: str
):

    for label, pattern in (
        FORBIDDEN_CODE_PATTERNS.items()
    ):

        if re.search(
            pattern,
            code,
            flags=re.IGNORECASE
        ):

            raise AIProviderResponseError(
                "Generated automation contains "
                f"forbidden {label}"
            )
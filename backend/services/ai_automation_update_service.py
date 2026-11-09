import json

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

from backend.models.automation_ai_update import (
    AutomationAIUpdateRequest,
)

from backend.models.automation_input_schema import (
    AutomationInputSchema,
)


AUTOMATION_UPDATE_SYSTEM_PROMPT = """
You are QualiAgent's senior web automation
engineer.

You are updating an EXISTING approved
Playwright JavaScript automation.

Do not redesign the Test Case.

Apply only changes that are appropriate for
the supplied Test Case, existing automation
source and human update instruction.

The result remains Playwright JavaScript.

Use:

const { test, expect } =
  require('@playwright/test');

Runtime inputs must continue to use:

process.env.KEY

Use only runtime input keys defined by the
supplied persisted input schema.

Never invent new environment variable names.

Never hard-code passwords, tokens, usernames,
URLs or other runtime values into the source.

Do not use:
- child_process
- shell commands
- filesystem access
- eval
- Function()
- arbitrary package imports

Return exactly one JSON object:

{
  "test_case_id": "existing Test Case ID",
  "framework": "playwright",
  "language": "javascript",
  "code": "complete updated JavaScript",
  "used_inputs": [
    "BASE_URL"
  ]
}

Do not return Markdown fences.
Do not return commentary outside the JSON.
""".strip()


def update_automation_with_ai(
    *,
    automation,
    test_case,
    requirement,
    scenario,
    project,
    request: AutomationAIUpdateRequest
) -> AIAutomationGeneration:

    if not automation.input_schema:

        raise AIProviderResponseError(
            "Source automation version does "
            "not contain a persisted input "
            "schema"
        )


    input_schema = (
        AutomationInputSchema
        .model_validate(
            automation.input_schema
        )
    )


    payload = {
        "project": {
            "name":
                getattr(
                    project,
                    "name",
                    ""
                )
        },

        "requirement": {
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
        },

        "scenario": {
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
        },

        "test_case": {
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

            "preconditions":
                getattr(
                    test_case,
                    "preconditions",
                    []
                ) or [],

            "test_data":
                getattr(
                    test_case,
                    "test_data",
                    []
                ) or [],

            "steps":
                getattr(
                    test_case,
                    "steps",
                    []
                ) or [],
        },

        "persisted_input_schema":
            input_schema.model_dump(),

        "existing_automation": {
            "version":
                automation.version,

            "engine":
                automation.engine,

            "language":
                automation.language,

            "code":
                automation.code,
        },

        "human_update_instruction":
            request.instruction,
    }


    provider = get_ai_provider()


    raw_result = provider.generate(
        system_prompt=(
            AUTOMATION_UPDATE_SYSTEM_PROMPT
        ),

        user_prompt=(
            "Update this existing automation "
            "according to the supplied human "
            "instruction.\n\n"
            + json.dumps(
                payload,
                ensure_ascii=False,
                indent=2
            )
        ),

        task="automation_update"
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
            "AI automation update did not "
            "match the required schema: "
            f"{exc}"
        ) from exc


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
            "AI update returned a different "
            "Test Case ID"
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
            "AI update uses unapproved "
            "runtime input keys: "
            + ", ".join(
                sorted(
                    unexpected_keys
                )
            )
        )


    for key in used_keys:

        reference = (
            f"process.env.{key}"
        )

        if reference not in generated.code:

            raise AIProviderResponseError(
                "AI updated automation must "
                "reference runtime input "
                f"'{key}' through "
                f"'{reference}'"
            )


    return generated
import json

from pydantic import ValidationError

from backend.ai.errors import (
    AIProviderResponseError,
)

from backend.ai.factory import (
    get_ai_provider,
)

from backend.models.automation_input_schema import (
    AutomationInputSchema,
)


AUTOMATION_INPUT_SYSTEM_PROMPT = """
You are QualiAgent's senior QA automation
input analyst.

Your task is to identify the runtime input
data required to automate exactly one
approved Test Case.

Use only:

1. The supplied Project context.
2. The supplied Requirement.
3. The selected Test Scenario.
4. The approved Test Case.
5. Its preconditions, test-data
   requirements, steps and expected
   results.

Do not generate automation code.

Do not generate Playwright selectors.

Do not generate actual values, usernames,
passwords, tokens, credentials, personal
data, URLs, production data or secrets.

Describe only the input fields that a
human tester must supply before automation
script generation or execution.

Return exactly one JSON object using this
structure:

{
  "test_case_id": "REQ-001-SCN-001-TC-001",
  "inputs": [
    {
      "key": "BASE_URL",
      "label": "Application URL",
      "input_type": "url",
      "required": true,
      "secret": false,
      "scope": "project",
      "description": "URL of the application under test",
      "placeholder": "Enter application URL"
    }
  ]
}

Allowed input_type values:

text
password
url
number
email
boolean
textarea

Allowed scope values:

project
execution

Rules:

1. The returned test_case_id must exactly
   match the supplied Test Case ID.

2. Input keys must use environment-variable
   format:

   BASE_URL
   TEST_USERNAME
   TEST_PASSWORD
   SEARCH_TERM
   PRODUCT_ID
   API_BASE_URL
   AUTH_TOKEN

3. Keys must begin with a letter and contain
   only uppercase letters, numbers and
   underscores.

4. Every key must be unique.

5. Use project scope only for reusable,
   non-secret project configuration such as:

   BASE_URL
   API_BASE_URL
   ENVIRONMENT_NAME

6. Use execution scope for credentials,
   scenario-specific data, expected values
   and one-run data.

7. Every secret must use execution scope.

8. Password fields must use:

   input_type = password
   secret = true
   scope = execution

9. Authentication tokens and API keys must
   use:

   secret = true
   scope = execution

10. Do not include an actual input value.

11. Do not include a default value.

12. Do not invent fields that are unrelated
    to the selected Test Case.

13. If a Test Case requires no tester-supplied
    runtime data, return an empty inputs list.

14. Do not include Markdown.

15. Do not return text outside the JSON
    object.

16. Do not assume that a login identifier
    is an email address.

17. If the supplied Requirement, Scenario
    or Test Case explicitly identifies the
    login field as a username, use:

    key = TEST_USERNAME
    label = Username
    input_type = text

18. If the supplied context explicitly
    identifies the login field as an email
    address, use:

    key = TEST_EMAIL
    label = Email Address
    input_type = email

19. If the supplied context only refers to
    a user identifier, login identifier,
    account identifier or credentials
    without stating its exact format, use:

    key = LOGIN_IDENTIFIER
    label = Login Identifier
    input_type = text

20. Never infer input_type=email merely
    because the input represents a user
    identity.

21. Labels and descriptions must preserve
    the terminology used by the Requirement,
    Scenario and Test Case wherever possible.
""".strip()


def build_automation_input_prompt(
    project,
    requirement,
    scenario,
    test_case
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

        "automation_candidate":
            bool(
                getattr(
                    test_case,
                    "automation_candidate",
                    False
                )
            ),

        "review_status":
            getattr(
                test_case,
                "review_status",
                "draft"
            ),
    }


    payload = {
        "project":
            project_payload,

        "requirement":
            requirement_payload,

        "selected_scenario":
            scenario_payload,

        "approved_test_case":
            test_case_payload,
    }


    return (
        "Identify the runtime input schema "
        "required to automate this approved "
        "QualiAgent Test Case.\n\n"
        + json.dumps(
            payload,
            ensure_ascii=False,
            indent=2
        )
    )
def ensure_application_endpoint(
    schema: AutomationInputSchema,
    project
) -> AutomationInputSchema:

    application_type = str(
        getattr(
            project,
            "application_type",
            ""
        )
    ).strip().lower()


    payload = schema.model_dump()


    existing_keys = {
        item["key"]
        for item in payload["inputs"]
    }


    if (
        application_type == "web" and
        "BASE_URL" not in existing_keys
    ):

        payload["inputs"].insert(
            0,
            {
                "key": "BASE_URL",
                "label": "Application URL",
                "input_type": "url",
                "required": True,
                "secret": False,
                "scope": "project",
                "description": (
                    "Base URL of the web "
                    "application under test"
                ),
                "placeholder": (
                    "Enter application URL"
                ),
            }
        )


    if (
        application_type == "api" and
        "API_BASE_URL" not in existing_keys
    ):

        payload["inputs"].insert(
            0,
            {
                "key": "API_BASE_URL",
                "label": "API Base URL",
                "input_type": "url",
                "required": True,
                "secret": False,
                "scope": "project",
                "description": (
                    "Base URL of the API "
                    "under test"
                ),
                "placeholder": (
                    "Enter API base URL"
                ),
            }
        )


    return AutomationInputSchema.model_validate(
        payload
    )

def normalise_login_identifier(
    schema: AutomationInputSchema,
    requirement,
    scenario,
    test_case
) -> AutomationInputSchema:

    payload = schema.model_dump()

    context_text = " ".join([
        str(
            getattr(
                requirement,
                "title",
                ""
            )
        ),
        str(
            getattr(
                requirement,
                "description",
                ""
            )
        ),
        str(
            getattr(
                scenario,
                "title",
                ""
            )
        ),
        str(
            getattr(
                scenario,
                "description",
                ""
            )
        ),
        str(
            getattr(
                test_case,
                "title",
                ""
            )
        ),
        " ".join(
            getattr(
                test_case,
                "test_data",
                []
            ) or []
        ),
    ]).lower()


    explicitly_email = any(
        phrase in context_text
        for phrase in [
            "email address",
            "e-mail address",
            "email login",
            "login with email",
        ]
    )


    explicitly_username = any(
        phrase in context_text
        for phrase in [
            "username",
            "user name",
            "login name",
        ]
    )


    for item in payload["inputs"]:

        key = str(
            item.get(
                "key",
                ""
            )
        ).upper()

        label = str(
            item.get(
                "label",
                ""
            )
        ).lower()


        looks_like_login_identifier = (
            key in {
                "TEST_EMAIL",
                "LOGIN_EMAIL",
                "EMAIL",
                "TEST_USERNAME",
                "USERNAME",
                "LOGIN_IDENTIFIER",
            }
            or "login email" in label
            or label == "email address"
            or "username" in label
        )


        if not looks_like_login_identifier:
            continue


        if explicitly_email:

            item["key"] = "TEST_EMAIL"
            item["label"] = "Email Address"
            item["input_type"] = "email"
            item["description"] = (
                "Valid email address for "
                "the test account"
            )

            continue


        if explicitly_username:

            item["key"] = "TEST_USERNAME"
            item["label"] = "Username"
            item["input_type"] = "text"
            item["description"] = (
                "Valid username for "
                "the test account"
            )

            continue


        item["key"] = "LOGIN_IDENTIFIER"
        item["label"] = "Login Identifier"
        item["input_type"] = "text"
        item["description"] = (
            "Valid login identifier for "
            "the test account"
        )


    return (
        AutomationInputSchema
        .model_validate(
            payload
        )
    )

def analyse_automation_inputs_with_ai(
    project,
    requirement,
    scenario,
    test_case
) -> AutomationInputSchema:

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
            "before automation input analysis"
        )


    if not bool(
        getattr(
            test_case,
            "automation_candidate",
            False
        )
    ):

        raise AIProviderResponseError(
            "Test Case is not marked as an "
            "automation candidate"
        )


    requirement_db_id = getattr(
        requirement,
        "id",
        None
    )

    scenario_requirement_db_id = getattr(
        scenario,
        "requirement_db_id",
        None
    )

    test_case_requirement_db_id = getattr(
        test_case,
        "requirement_db_id",
        None
    )

    test_case_scenario_db_id = getattr(
        test_case,
        "test_scenario_db_id",
        None
    )


    if (
        scenario_requirement_db_id !=
        requirement_db_id
    ):

        raise AIProviderResponseError(
            "Scenario does not belong to "
            "the supplied Requirement"
        )


    if (
        test_case_requirement_db_id !=
        requirement_db_id
    ):

        raise AIProviderResponseError(
            "Test Case does not belong to "
            "the supplied Requirement"
        )


    if (
        test_case_scenario_db_id !=
        getattr(
            scenario,
            "id",
            None
        )
    ):

        raise AIProviderResponseError(
            "Test Case does not belong to "
            "the supplied Scenario"
        )


    provider = get_ai_provider()


    raw_result = provider.generate(
        system_prompt=(
            AUTOMATION_INPUT_SYSTEM_PROMPT
        ),

        user_prompt=(
            build_automation_input_prompt(
                project,
                requirement,
                scenario,
                test_case
            )
        ),

        task="automation_input_analysis"
    )


    try:

        validated = (
            AutomationInputSchema
            .model_validate(
                raw_result
            )
        )

    except ValidationError as exc:

        raise AIProviderResponseError(
            "AI automation-input analysis "
            "did not match the required "
            f"schema: {exc}"
        ) from exc


    expected_test_case_id = str(
        getattr(
            test_case,
            "test_case_id",
            ""
        )
    ).strip()


    if (
        validated.test_case_id !=
        expected_test_case_id
    ):

        raise AIProviderResponseError(
            "AI automation-input analysis "
            "returned a different "
            "test_case_id"
        )
    
    sensitive_key_parts = {
    "PASSWORD",
    "PASSCODE",
    "SECRET",
    "TOKEN",
    "API_KEY",
    "ACCESS_KEY",
    "PRIVATE_KEY",
}


    for item in validated.inputs:

      is_sensitive_key = any(
        part in item.key
        for part in sensitive_key_parts
    )

    if (
        is_sensitive_key and
        not item.secret
    ):

        raise AIProviderResponseError(
            "Sensitive automation input "
            f"'{item.key}' must be marked "
            "as secret"
        )


    if (
        item.secret and
        item.scope != "execution"
    ):

        raise AIProviderResponseError(
            "Secret automation input "
            f"'{item.key}' must use "
            "execution scope"
        )

    validated = (
    normalise_login_identifier(
        validated,
        requirement,
        scenario,
        test_case
    )
)

    validated = (
    ensure_application_endpoint(
        validated,
        project
    )
)

    return validated
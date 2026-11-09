from backend.models.execution_runtime import (
    ExecutionRuntimeRequest,
)

from backend.services.automation_runtime_input_service import (
    get_persisted_input_schema,
    validate_runtime_inputs,
)


def prepare_execution_runtime(
    *,
    project,
    requirement,
    scenario,
    test_case,
    automation,
    request: ExecutionRuntimeRequest
):

    project_engine = str(
        project.automation_engine or ""
    ).strip().lower()


    automation_engine = str(
        automation.engine or
        automation.framework or
        ""
    ).strip().lower()

    project_language = str(
        project.automation_language or ""
    ).strip().lower()


    automation_language = str(
        automation.language or ""
    ).strip().lower()


    if automation_engine != project_engine:

        raise ValueError(
            "Automation engine does not match "
            "the Project automation engine"
        )

    if (
        automation_language !=
        project_language
    ):

        raise ValueError(
            "Automation language does not "
            "match the Project automation "
            "language"
        )

    automation_status = str(
        getattr(
            automation,
            "status",
            ""
        )
    ).strip().lower()


    if automation_status != "ready":

        raise ValueError(
            "Automation must be READY "
            "before execution"
        )


    review_status = str(
        getattr(
            test_case,
            "review_status",
            ""
        )
    ).strip().lower()


    if review_status != "approved":

        raise ValueError(
            "Parent Test Case must remain "
            "approved before execution"
        )


    execution_type = str(
        getattr(
            test_case,
            "execution_type",
            "manual"
        )
        or "manual"
    ).strip().lower()


    if execution_type not in {
        "automation",
        "both",
    }:

        raise ValueError(
            "Test Case must be classified "
            "as AUTOMATION or BOTH before "
            "automated execution"
        )


    if (
        getattr(
            scenario,
            "requirement_db_id",
            None
        ) != getattr(
            requirement,
            "id",
            None
        )
    ):

        raise ValueError(
            "Scenario and Requirement "
            "traceability is inconsistent"
        )


    if (
        getattr(
            test_case,
            "requirement_db_id",
            None
        ) != getattr(
            requirement,
            "id",
            None
        )
    ):

        raise ValueError(
            "Test Case and Requirement "
            "traceability is inconsistent"
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

        raise ValueError(
            "Test Case and Scenario "
            "traceability is inconsistent"
        )


    input_schema = (
        get_persisted_input_schema(
            automation
        )
    )


    validated_inputs = (
        validate_runtime_inputs(
            input_schema,
            request
        )
    )


    return (
        input_schema,
        validated_inputs
    )

def build_execution_environment(
    validated_inputs
) -> dict[str, str]:

    environment = {}


    for key, value in (
        validated_inputs
        .non_secret_values
        .items()
    ):

        environment[key] = (
            normalise_environment_value(
                value
            )
        )


    for key, value in (
        validated_inputs
        .secret_values
        .items()
    ):

        environment[key] = str(
            value
        )


    return environment


def normalise_environment_value(
    value
) -> str:

    if isinstance(value, bool):

        return (
            "true"
            if value
            else "false"
        )


    return str(
        value
    )
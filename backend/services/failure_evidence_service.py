from sqlalchemy.orm import Session


from backend.db.automation_model import (
    AutomationScriptDB,
)

from backend.db.execution_model import (
    ExecutionDB,
)

from backend.db.project_model import (
    ProjectDB,
)

from backend.db.requirement_model import (
    RequirementDB,
)

from backend.db.test_case_model import (
    TestCaseDB,
)

from backend.db.test_scenario_model import (
    TestScenarioDB,
)

from backend.models.failure_analysis import (
    FailureAutomationContext,
    FailureEvidencePackage,
    FailureTestContext,
)

from backend.services.failure_analysis_policy import (
    MAX_AUTOMATION_CODE_LENGTH,
    MAX_ERROR_EXCERPT_LENGTH,
    MAX_OUTPUT_EXCERPT_LENGTH,
    ensure_execution_can_be_analysed,
    normalise_status,
    redact_and_excerpt,
)


def clean_text(
    value,
    default: str = ""
) -> str:

    if value is None:

        return default


    cleaned = str(
        value
    ).strip()


    return (
        cleaned
        if cleaned
        else default
    )


def has_path(
    value
) -> bool:

    if value is None:

        return False


    return bool(
        str(
            value
        ).strip()
    )


def get_first_available_attribute(
    source,
    names: list[str]
):

    for name in names:

        if not hasattr(
            source,
            name
        ):

            continue


        value = getattr(
            source,
            name
        )


        if value is not None:

            return value


    return None


def get_execution_error_text(
    execution
):

    return get_first_available_attribute(
        execution,
        [
            "error_message",
            "error",
            "stderr",
            "failure_message",
        ]
    )


def get_execution_output_text(
    execution
):

    return get_first_available_attribute(
        execution,
        [
            "stdout",
            "output",
            "console_output",
            "runner_output",
        ]
    )


def collect_failure_evidence(
    db: Session,
    execution_id: int
) -> FailureEvidencePackage:

    execution = (
        db.query(
            ExecutionDB
        )
        .filter(
            ExecutionDB.id ==
            execution_id
        )
        .first()
    )


    if execution is None:

        raise ValueError(
            "Execution not found"
        )


    ensure_execution_can_be_analysed(
        execution
    )


    automation_version_id = (
        get_first_available_attribute(
            execution,
            [
                "automation_script_id",
                "automation_version_id",
            ]
        )
    )


    automation = None


    if automation_version_id is not None:

        automation = (
            db.query(
                AutomationScriptDB
            )
            .filter(
                AutomationScriptDB.id ==
                automation_version_id
            )
            .first()
        )


    if automation is None:

        raise ValueError(
            (
                "The failed Execution is not "
                "linked to an Automation version."
            )
        )


    test_case_db_id = (
        automation.test_case_db_id
    )


    test_case = (
        db.query(
            TestCaseDB
        )
        .filter(
            TestCaseDB.id ==
            test_case_db_id
        )
        .first()
    )


    if test_case is None:

        raise ValueError(
            "Parent Test Case not found"
        )


    scenario = (
        db.query(
            TestScenarioDB
        )
        .filter(
            TestScenarioDB.id ==
            test_case.test_scenario_db_id
        )
        .first()
    )


    if scenario is None:

        raise ValueError(
            "Parent Scenario not found"
        )


    requirement = (
        db.query(
            RequirementDB
        )
        .filter(
            RequirementDB.id ==
            scenario.requirement_db_id
        )
        .first()
    )


    if requirement is None:

        raise ValueError(
            "Parent Requirement not found"
        )


    project = (
        db.query(
            ProjectDB
        )
        .filter(
            ProjectDB.id ==
            requirement.project_id
        )
        .first()
    )


    if project is None:

        raise ValueError(
            "Parent Project not found"
        )


    raw_error = (
        get_execution_error_text(
            execution
        )
    )


    raw_output = (
        get_execution_output_text(
            execution
        )
    )


    raw_code = (
        automation.code
    )


    error_result = (
        redact_and_excerpt(
            raw_error,
            MAX_ERROR_EXCERPT_LENGTH
        )
    )


    output_result = (
        redact_and_excerpt(
            raw_output,
            MAX_OUTPUT_EXCERPT_LENGTH
        )
    )


    code_result = (
        redact_and_excerpt(
            raw_code,
            MAX_AUTOMATION_CODE_LENGTH
        )
    )


    total_redactions = (
        error_result.redaction_count
        +
        output_result.redaction_count
        +
        code_result.redaction_count
    )


    screenshot_available = (
        has_path(
            execution.screenshot_path
        )
    )


    trace_available = (
        has_path(
            execution.trace_path
        )
    )


    return FailureEvidencePackage(
        execution_id=execution.id,

        execution_status=(
            normalise_status(
                execution.status
            )
        ),

        exit_code=(
            execution.exit_code
        ),

        duration_ms=(
            execution.duration_ms
        ),

        screenshot_available=(
            screenshot_available
        ),

        trace_available=(
            trace_available
        ),

        error_excerpt=(
            error_result.text
        ),

        output_excerpt=(
            output_result.text
        ),

        test_context=(
            FailureTestContext(
                project_id=project.id,

                project_name=clean_text(
                    project.name,
                    f"Project {project.id}"
                ),

                requirement_id=clean_text(
                    requirement.requirement_id,
                    str(
                        requirement.id
                    )
                ),

                requirement_title=clean_text(
                    requirement.title,
                    "Untitled Requirement"
                ),

                scenario_id=clean_text(
                    scenario.scenario_id,
                    str(
                        scenario.id
                    )
                ),

                scenario_title=clean_text(
                    scenario.title,
                    "Untitled Scenario"
                ),

                test_case_db_id=(
                    test_case.id
                ),

                test_case_id=clean_text(
                    test_case.test_case_id,
                    str(
                        test_case.id
                    )
                ),

                test_case_title=clean_text(
                    test_case.title,
                    "Untitled Test Case"
                ),

                test_case_type=(
                    test_case.test_type
                ),

                test_case_priority=(
                    test_case.priority
                )
            )
        ),

        automation_context=(
            FailureAutomationContext(
                automation_version_id=(
                    automation.id
                ),

                version_number=(
                    automation.version
                ),

                framework=(
                    automation.framework
                ),

                engine=(
                    automation.engine
                ),

                language=(
                    automation.language
                ),

                status=clean_text(
                    automation.status,
                    "unknown"
                ),

                source=(
                    automation.source
                ),

                parent_version_id=(
                    automation.parent_version_id
                ),

                code_excerpt=(
                    code_result.text
                )
            )
        ),

        redaction_applied=(
            total_redactions > 0
        ),

        redaction_count=(
            total_redactions
        ),

        evidence_paths_exposed=False,

        runtime_secrets_included=False
    )
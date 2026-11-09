from sqlalchemy.orm import Session

from backend.db.automation_model import (
    AutomationScriptDB,
)

from backend.db.execution_model import (
    ExecutionDB,
)

from backend.services.execution_environment_service import (
    get_environment_secrets,
    redact_text,
)

from backend.services.execution_service import (
    mark_execution_error,
    mark_execution_failed,
    mark_execution_passed,
    mark_execution_running,
)


def run_execution(
    db: Session,
    execution: ExecutionDB,
    automation: AutomationScriptDB,
    engine,
    runtime_environment: dict[str, str]
):

    # Validate before the execution is
    # persisted as RUNNING.
    engine.validate_source(
        automation.code
    )


    mark_execution_running(
        db,
        execution
    )


    secrets = get_environment_secrets(
        runtime_environment
    )


    result = engine.execute(
        automation=automation,
        execution=execution,
        runtime_inputs=runtime_environment
    )


    safe_stdout = redact_text(
        result.stdout,
        secrets
    )


    safe_stderr = redact_text(
        result.stderr,
        secrets
    )


    safe_infrastructure_error = redact_text(
        result.infrastructure_error,
        secrets
    )


    if result.infrastructure_error:

        return mark_execution_error(
            db=db,
            execution=execution,
            completed_at=(
                result.completed_at
            ),
            duration_ms=(
                result.duration_ms
            ),
            error_message=(
                safe_infrastructure_error
            ),
            stdout=safe_stdout,
            stderr=safe_stderr,
            screenshot_path=(
                result.screenshot_path
            ),
            trace_path=(
                result.trace_path
            )
        )


    if result.exit_code == 0:

        return mark_execution_passed(
            db=db,
            execution=execution,
            completed_at=(
                result.completed_at
            ),
            duration_ms=(
                result.duration_ms
            ),
            exit_code=0,
            stdout=safe_stdout,
            stderr=safe_stderr,
            screenshot_path=(
                result.screenshot_path
            ),
            trace_path=(
                result.trace_path
            )
        )


    return mark_execution_failed(
        db=db,
        execution=execution,
        completed_at=(
            result.completed_at
        ),
        duration_ms=(
            result.duration_ms
        ),
        exit_code=(
            result.exit_code
            if result.exit_code is not None
            else -1
        ),
        stdout=safe_stdout,
        stderr=safe_stderr,
        screenshot_path=(
            result.screenshot_path
        ),
        trace_path=(
            result.trace_path
        )
    )
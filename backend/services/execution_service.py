from datetime import datetime
from sqlalchemy.orm import Session

from backend.db.automation_model import (
    AutomationScriptDB,
)
from backend.db.execution_model import (
    ExecutionDB,
)
from backend.db.requirement_model import (
    RequirementDB,
)

from backend.db.test_case_model import (
    TestCaseDB,
)


def get_automation_script(
    db: Session,
    automation_script_id: int
):

    return (
        db.query(AutomationScriptDB)
        .filter(
            AutomationScriptDB.id ==
            automation_script_id
        )
        .first()
    )


def create_execution(
    db: Session,
    automation_script_id: int
):

    execution = ExecutionDB(
        automation_script_id=(
            automation_script_id
        ),
        status="pending"
    )

    db.add(execution)

    db.commit()

    db.refresh(execution)

    return execution


def get_execution(
    db: Session,
    execution_id: int
):

    return (
        db.query(ExecutionDB)
        .filter(
            ExecutionDB.id ==
            execution_id
        )
        .first()
    )


def get_automation_executions(
    db: Session,
    automation_script_id: int
):

    return (
        db.query(ExecutionDB)
        .filter(
            ExecutionDB.automation_script_id ==
            automation_script_id
        )
        .order_by(
            ExecutionDB.id.desc()
        )
        .all()
    )

def mark_execution_running(
    db: Session,
    execution: ExecutionDB
):

    execution.status = "running"
    execution.started_at = datetime.utcnow()

    execution.completed_at = None
    execution.duration_ms = None
    execution.exit_code = None
    execution.stdout = None
    execution.stderr = None
    execution.error_message = None

    db.commit()
    db.refresh(execution)

    return execution


def mark_execution_passed(
    db: Session,
    execution: ExecutionDB,
    completed_at: datetime,
    duration_ms: int,
    exit_code: int,
    stdout: str,
    stderr: str,
    screenshot_path: str | None = None,
    trace_path: str | None = None
    
):

    execution.status = "passed"
    execution.completed_at = completed_at
    execution.duration_ms = duration_ms
    execution.exit_code = exit_code
    execution.stdout = stdout
    execution.stderr = stderr
    execution.error_message = None
    execution.screenshot_path = (
    screenshot_path)
    execution.trace_path = (
    trace_path
)

    db.commit()
    db.refresh(execution)

    return execution


def mark_execution_failed(
    db: Session,
    execution: ExecutionDB,
    completed_at: datetime,
    duration_ms: int,
    exit_code: int,
    stdout: str,
    stderr: str,
    screenshot_path: str | None = None,
    trace_path: str | None = None
):

    execution.status = "failed"
    execution.completed_at = completed_at
    execution.duration_ms = duration_ms
    execution.exit_code = exit_code
    execution.stdout = stdout
    execution.stderr = stderr

    execution.error_message = (
        "Playwright completed with "
        f"exit code {exit_code}"
    )
    execution.screenshot_path = (
    screenshot_path
)

    execution.trace_path = (
    trace_path
)

    db.commit()
    db.refresh(execution)

    return execution


def mark_execution_error(
    db: Session,
    execution: ExecutionDB,
    completed_at: datetime,
    duration_ms: int,
    error_message: str,
    stdout: str = "",
    stderr: str = "",
    screenshot_path: str | None = None,
    trace_path: str | None = None
):

    execution.status = "error"
    execution.completed_at = completed_at
    execution.duration_ms = duration_ms
    execution.exit_code = None
    execution.stdout = stdout
    execution.stderr = stderr
    execution.error_message = error_message
    execution.screenshot_path = (
    screenshot_path
)

    execution.trace_path = (
    trace_path
)

    db.commit()
    db.refresh(execution)

    return execution

def get_execution_automation(
    db: Session,
    execution: ExecutionDB
):

    return (
        db.query(AutomationScriptDB)
        .filter(
            AutomationScriptDB.id ==
            execution.automation_script_id
        )
        .first()
    ) 

def get_project_executions(
    db: Session,
    project_id: int
):

    rows = (
        db.query(
            ExecutionDB,
            AutomationScriptDB,
            TestCaseDB,
            RequirementDB
        )
        .join(
            AutomationScriptDB,
            ExecutionDB.automation_script_id
            == AutomationScriptDB.id
        )
        .join(
            TestCaseDB,
            AutomationScriptDB.test_case_db_id
            == TestCaseDB.id
        )
        .join(
            RequirementDB,
            TestCaseDB.requirement_db_id
            == RequirementDB.id
        )
        .filter(
            RequirementDB.project_id
            == project_id
        )
        .order_by(
            ExecutionDB.id.desc()
        )
        .all()
    )

    return rows

def build_project_execution_response(
    row
):

    (
        execution,
        automation,
        test_case,
        requirement
    ) = row

    return {
        "id":
            execution.id,

        "automation_script_id":
            execution.automation_script_id,

        "status":
            execution.status,

        "started_at":
            execution.started_at,

        "completed_at":
            execution.completed_at,

        "duration_ms":
            execution.duration_ms,

        "exit_code":
            execution.exit_code,

        "stdout":
            execution.stdout,

        "stderr":
            execution.stderr,

        "error_message":
            execution.error_message,

        "screenshot_path":
            execution.screenshot_path,

        "trace_path":
            execution.trace_path,

        "created_at":
            execution.created_at,

        "test_case_db_id":
            test_case.id,

        "test_case_id":
            test_case.test_case_id,

        "test_case_title":
            test_case.title,

        "requirement_id":
            requirement.requirement_id,

        "framework":
            automation.framework,

        "language":
            automation.language
    }

    
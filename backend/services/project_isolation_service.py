from sqlalchemy.orm import Session

from backend.db.project_model import (
    ProjectDB,
)

from backend.db.requirement_model import (
    RequirementDB,
)

from backend.db.test_case_model import (
    TestCaseDB,
)

from backend.db.automation_model import (
    AutomationScriptDB,
)

from backend.db.execution_model import (
    ExecutionDB,
)


class ProjectIsolationError(
    ValueError
):
    pass


def get_project_or_404(
    db: Session,
    project_id: int
) -> ProjectDB:

    project = (
        db.query(
            ProjectDB
        )
        .filter(
            ProjectDB.id ==
            project_id
        )
        .first()
    )


    if project is None:

        raise ProjectIsolationError(
            "Resource not found"
        )


    return project


def require_requirement_in_project(
    db: Session,
    *,
    project_id: int,
    requirement_db_id: int
) -> RequirementDB:

    requirement = (
        db.query(
            RequirementDB
        )
        .filter(
            RequirementDB.id ==
            requirement_db_id,

            RequirementDB.project_id ==
            project_id
        )
        .first()
    )


    if requirement is None:

        raise ProjectIsolationError(
            "Resource not found"
        )


    return requirement


def require_test_case_in_project(
    db: Session,
    *,
    project_id: int,
    test_case_db_id: int
) -> TestCaseDB:

    test_case = (
        db.query(
            TestCaseDB
        )
        .join(
            RequirementDB,
            TestCaseDB.requirement_db_id ==
            RequirementDB.id
        )
        .filter(
            TestCaseDB.id ==
            test_case_db_id,

            RequirementDB.project_id ==
            project_id
        )
        .first()
    )


    if test_case is None:

        raise ProjectIsolationError(
            "Resource not found"
        )


    return test_case


def require_automation_in_project(
    db: Session,
    *,
    project_id: int,
    automation_id: int
) -> AutomationScriptDB:

    automation = (
        db.query(
            AutomationScriptDB
        )
        .join(
            TestCaseDB,
            AutomationScriptDB.test_case_db_id ==
            TestCaseDB.id
        )
        .join(
            RequirementDB,
            TestCaseDB.requirement_db_id ==
            RequirementDB.id
        )
        .filter(
            AutomationScriptDB.id ==
            automation_id,

            RequirementDB.project_id ==
            project_id
        )
        .first()
    )


    if automation is None:

        raise ProjectIsolationError(
            "Resource not found"
        )


    return automation


def require_execution_in_project(
    db: Session,
    *,
    project_id: int,
    execution_id: int
) -> ExecutionDB:

    execution = (
        db.query(
            ExecutionDB
        )
        .join(
            AutomationScriptDB,
            ExecutionDB.automation_script_id ==
            AutomationScriptDB.id
        )
        .join(
            TestCaseDB,
            AutomationScriptDB.test_case_db_id ==
            TestCaseDB.id
        )
        .join(
            RequirementDB,
            TestCaseDB.requirement_db_id ==
            RequirementDB.id
        )
        .filter(
            ExecutionDB.id ==
            execution_id,

            RequirementDB.project_id ==
            project_id
        )
        .first()
    )


    if execution is None:

        raise ProjectIsolationError(
            "Resource not found"
        )


    return execution
from sqlalchemy import func
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


def get_project(
    db: Session,
    project_id: int
):

    return (
        db.query(ProjectDB)
        .filter(
            ProjectDB.id ==
            project_id
        )
        .first()
    )


def get_requirement_count(
    db: Session,
    project_id: int
):

    return (
        db.query(
            func.count(
                RequirementDB.id
            )
        )
        .filter(
            RequirementDB.project_id ==
            project_id
        )
        .scalar()
        or 0
    )


def project_test_case_query(
    db: Session,
    project_id: int
):

    return (
        db.query(TestCaseDB)
        .join(
            RequirementDB,
            TestCaseDB.requirement_db_id
            == RequirementDB.id
        )
        .filter(
            RequirementDB.project_id ==
            project_id
        )
    )


def count_test_cases(
    db: Session,
    project_id: int,
    review_status: str | None = None
):

    query = project_test_case_query(
        db,
        project_id
    )

    if review_status is not None:

        query = query.filter(
            TestCaseDB.review_status ==
            review_status
        )

    return query.count()


def count_automation_candidates(
    db: Session,
    project_id: int
):

    return (
        project_test_case_query(
            db,
            project_id
        )
        .filter(
            TestCaseDB.automation_candidate
            .is_(True)
        )
        .count()
    )


def project_automation_query(
    db: Session,
    project_id: int
):

    return (
        db.query(
            AutomationScriptDB
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
            RequirementDB.project_id ==
            project_id
        )
    )


def count_ready_automation(
    db: Session,
    project_id: int
):

    return (
        project_automation_query(
            db,
            project_id
        )
        .filter(
            AutomationScriptDB.status ==
            "ready"
        )
        .count()
    )


def project_execution_query(
    db: Session,
    project_id: int
):

    return (
        db.query(
            ExecutionDB
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
            RequirementDB.project_id ==
            project_id
        )
    )


def count_executions(
    db: Session,
    project_id: int,
    status: str | None = None
):

    query = project_execution_query(
        db,
        project_id
    )

    if status is not None:

        query = query.filter(
            ExecutionDB.status ==
            status
        )

    return query.count()


def calculate_pass_rate(
    passed: int,
    failed: int
) -> float:

    completed = (
        passed +
        failed
    )

    if completed == 0:
        return 0.0

    return round(
        (
            passed /
            completed
        ) *
        100,
        2
    )


def get_project_quality_summary(
    db: Session,
    project: ProjectDB
):

    project_id = project.id

    requirements = (
        get_requirement_count(
            db,
            project_id
        )
    )

    test_cases = count_test_cases(
        db,
        project_id
    )

    draft_tests = count_test_cases(
        db,
        project_id,
        "draft"
    )

    approved_tests = count_test_cases(
        db,
        project_id,
        "approved"
    )

    rejected_tests = count_test_cases(
        db,
        project_id,
        "rejected"
    )

    automation_candidates = (
        count_automation_candidates(
            db,
            project_id
        )
    )

    automation_ready = (
        count_ready_automation(
            db,
            project_id
        )
    )

    executions = count_executions(
        db,
        project_id
    )

    passed = count_executions(
        db,
        project_id,
        "passed"
    )

    failed = count_executions(
        db,
        project_id,
        "failed"
    )

    errors = count_executions(
        db,
        project_id,
        "error"
    )

    pass_rate = calculate_pass_rate(
        passed,
        failed
    )

    return {
        "project_id":
            project.id,

        "project_name":
            project.name,

        "requirements":
            requirements,

        "test_cases":
            test_cases,

        "draft_tests":
            draft_tests,

        "approved_tests":
            approved_tests,

        "rejected_tests":
            rejected_tests,

        "automation_candidates":
            automation_candidates,

        "automation_ready":
            automation_ready,

        "executions":
            executions,

        "passed":
            passed,

        "failed":
            failed,

        "errors":
            errors,

        "pass_rate":
            pass_rate
    }

def get_requirement_coverage(
    db: Session,
    project_id: int
):

    requirements = (
        db.query(RequirementDB)
        .filter(
            RequirementDB.project_id ==
            project_id
        )
        .order_by(
            RequirementDB.id.asc()
        )
        .all()
    )

    coverage = []

    for requirement in requirements:

        test_cases = (
            db.query(TestCaseDB)
            .filter(
                TestCaseDB.requirement_db_id
                == requirement.id
            )
            .all()
        )

        test_case_ids = [
            test_case.id
            for test_case in test_cases
        ]

        approved_tests = sum(
            1
            for test_case in test_cases
            if test_case.review_status ==
            "approved"
        )


        if test_case_ids:

            automation_scripts = (
                db.query(
                    AutomationScriptDB
                )
                .filter(
                    AutomationScriptDB
                    .test_case_db_id
                    .in_(test_case_ids)
                )
                .all()
            )

        else:

            automation_scripts = []


        ready_automation = [
            automation
            for automation in
            automation_scripts
            if automation.status == "ready"
        ]


        automation_ids = [
            automation.id
            for automation in
            automation_scripts
        ]


        if automation_ids:

            executions = (
                db.query(
                    ExecutionDB
                )
                .filter(
                    ExecutionDB
                    .automation_script_id
                    .in_(automation_ids)
                )
                .order_by(
                    ExecutionDB.id.desc()
                )
                .all()
            )

        else:

            executions = []


        latest_execution = (
            executions[0]
            if executions
            else None
        )


        coverage.append({
            "requirement_db_id":
                requirement.id,

            "requirement_id":
                requirement.requirement_id,

            "title":
                requirement.title,

            "test_cases":
                len(test_cases),

            "approved_tests":
                approved_tests,

            "automation_ready":
                len(ready_automation),

            "executions":
                len(executions),

            "latest_execution_id":
                (
                    latest_execution.id
                    if latest_execution
                    else None
                ),

            "latest_status":
                (
                    latest_execution.status
                    if latest_execution
                    else None
                )
        })

    return coverage
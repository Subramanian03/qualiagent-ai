from dataclasses import dataclass
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

from backend.db.test_scenario_model import (
    TestScenarioDB,
)

from backend.db.test_cycle_model import (
    TestCycleDB,
)

from backend.db.cycle_test_item_model import (
    CycleTestItemDB,
)

from backend.db.execution_config_model import (
    ExecutionConfigDB,
)


class ProjectIsolationError(
    ValueError
):
    pass

@dataclass(frozen=True)
class CycleItemProjectLinks:
    cycle: TestCycleDB
    test_case: TestCaseDB
    automation_version: AutomationScriptDB | None
    execution: ExecutionDB | None


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

def require_test_scenario_in_project(
    db: Session,
    *,
    project_id: int,
    test_scenario_db_id: int
) -> TestScenarioDB:

    scenario = (
        db.query(
            TestScenarioDB
        )
        .join(
            RequirementDB,
            TestScenarioDB.requirement_db_id
            == RequirementDB.id
        )
        .filter(
            TestScenarioDB.id
            == test_scenario_db_id,

            RequirementDB.project_id
            == project_id
        )
        .first()
    )

    if scenario is None:
        raise ProjectIsolationError(
            "Resource not found"
        )

    return scenario

def require_test_cycle_in_project(
    db: Session,
    *,
    project_id: int,
    cycle_id: int
) -> TestCycleDB:

    cycle = (
        db.query(
            TestCycleDB
        )
        .filter(
            TestCycleDB.id
            == cycle_id,

            TestCycleDB.project_id
            == project_id
        )
        .first()
    )

    if cycle is None:
        raise ProjectIsolationError(
            "Resource not found"
        )

    return cycle

def require_cycle_test_item_in_project(
    db: Session,
    *,
    project_id: int,
    cycle_item_id: int
) -> CycleTestItemDB:

    cycle_item = (
        db.query(
            CycleTestItemDB
        )
        .join(
            TestCycleDB,
            CycleTestItemDB.cycle_id
            == TestCycleDB.id
        )
        .filter(
            CycleTestItemDB.id
            == cycle_item_id,

            TestCycleDB.project_id
            == project_id
        )
        .first()
    )

    if cycle_item is None:
        raise ProjectIsolationError(
            "Resource not found"
        )

    return cycle_item

def require_execution_config_in_project(
    db: Session,
    *,
    project_id: int,
    execution_config_id: int
) -> ExecutionConfigDB:

    execution_config = (
        db.query(
            ExecutionConfigDB
        )
        .filter(
            ExecutionConfigDB.id
            == execution_config_id,

            ExecutionConfigDB.project_id
            == project_id
        )
        .first()
    )

    if execution_config is None:
        raise ProjectIsolationError(
            "Resource not found"
        )

    return execution_config

def require_cycle_item_links_in_project(
    db: Session,
    *,
    project_id: int,
    cycle_id: int,
    test_case_id: int,
    automation_version_id: int | None = None,
    execution_id: int | None = None
) -> CycleItemProjectLinks:

    cycle = require_test_cycle_in_project(
        db,
        project_id=project_id,
        cycle_id=cycle_id
    )

    test_case = require_test_case_in_project(
        db,
        project_id=project_id,
        test_case_db_id=test_case_id
    )

    automation_version: (
        AutomationScriptDB | None
    ) = None

    execution: ExecutionDB | None = None

    if automation_version_id is not None:
        automation_version = (
            require_automation_in_project(
                db,
                project_id=project_id,
                automation_id=automation_version_id
            )
        )

        if (
            automation_version.test_case_db_id
            != test_case.id
        ):
            raise ProjectIsolationError(
                "Resource not found"
            )

    if execution_id is not None:
        execution = require_execution_in_project(
            db,
            project_id=project_id,
            execution_id=execution_id
        )

        execution_automation = (
            require_automation_in_project(
                db,
                project_id=project_id,
                automation_id=(
                    execution.automation_script_id
                )
            )
        )

        if (
            execution_automation.test_case_db_id
            != test_case.id
        ):
            raise ProjectIsolationError(
                "Resource not found"
            )

        if (
            automation_version_id is not None
            and
            execution.automation_script_id
            != automation_version_id
        ):
            raise ProjectIsolationError(
                "Resource not found"
            )

    return CycleItemProjectLinks(
        cycle=cycle,
        test_case=test_case,
        automation_version=automation_version,
        execution=execution
    )
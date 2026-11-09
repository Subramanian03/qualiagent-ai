from sqlalchemy.orm import Session

from backend.db.execution_config_model import (
    ExecutionConfigDB,
)
from backend.db.project_model import (
    ProjectDB,
)
from backend.models.execution_config import (
    ExecutionConfigUpsert,
)
from backend.db.automation_model import (
    AutomationScriptDB,
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
            ProjectDB.id == project_id
        )
        .first()
    )


def get_execution_config(
    db: Session,
    project_id: int
):

    return (
        db.query(ExecutionConfigDB)
        .filter(
            ExecutionConfigDB.project_id ==
            project_id
        )
        .first()
    )


def upsert_execution_config(
    db: Session,
    project_id: int,
    request: ExecutionConfigUpsert
):

    config = get_execution_config(
        db,
        project_id
    )

    values = request.model_dump(
        mode="json"
    )

    if config is None:

        config = ExecutionConfigDB(
            project_id=project_id,
            **values
        )

        db.add(config)

    else:

        for field, value in values.items():
            setattr(
                config,
                field,
                value
            )

    db.commit()
    db.refresh(config)

    return config

def get_execution_config_for_automation(
    db: Session,
    automation_script_id: int
):

    return (
        db.query(ExecutionConfigDB)
        .join(
            RequirementDB,
            ExecutionConfigDB.project_id
            == RequirementDB.project_id
        )
        .join(
            TestCaseDB,
            TestCaseDB.requirement_db_id
            == RequirementDB.id
        )
        .join(
            AutomationScriptDB,
            AutomationScriptDB.test_case_db_id
            == TestCaseDB.id
        )
        .filter(
            AutomationScriptDB.id
            == automation_script_id
        )
        .first()
    )
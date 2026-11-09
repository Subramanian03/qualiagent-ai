from sqlalchemy.orm import Session
from sqlalchemy.orm import selectinload

from backend.db.automation_model import (
    AutomationScriptDB,
)

from backend.db.cycle_test_item_model import (
    CycleTestItemDB,
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

from backend.db.test_cycle_model import (
    TestCycleDB,
)

from backend.db.test_scenario_model import (
    TestScenarioDB,
)

from backend.models.test_cycle import (
    TestCycleCreate,
)

def has_persisted_input_schema(
    automation
) -> bool:

    if automation is None:
        return False


    input_schema = (
        automation.input_schema
    )


    if input_schema is None:
        return False


    if (
        isinstance(
            input_schema,
            str
        )
        and
        not input_schema.strip()
    ):
        return False


    return True

class TestCycleValidationError(
    ValueError
):
    pass


def normalise_text(
    value,
    default: str = ""
) -> str:

    return str(
        value
        if value is not None
        else default
    ).strip().lower()


def clean_optional_text(
    value
) -> str | None:

    if value is None:

        return None


    cleaned = str(
        value
    ).strip()


    return (
        cleaned
        if cleaned
        else None
    )


def get_compatible_ready_automation(
    db: Session,
    *,
    project: ProjectDB,
    test_case: TestCaseDB
) -> AutomationScriptDB | None:

    project_engine = normalise_text(
        project.automation_engine
    )


    project_language = normalise_text(
        project.automation_language
    )


    ready_versions = (
        db.query(
            AutomationScriptDB
        )
        .filter(
            AutomationScriptDB
            .test_case_db_id ==
            test_case.id,

            AutomationScriptDB.status ==
            "ready"
        )
        .order_by(
            AutomationScriptDB
            .version.desc(),

            AutomationScriptDB
            .id.desc()
        )
        .all()
    )


    for automation in ready_versions:

        automation_engine = (
            normalise_text(
                automation.engine
                or
                automation.framework
            )
        )


        automation_language = (
            normalise_text(
                automation.language
            )
        )


        if (
            automation_engine ==
            project_engine
            and
            automation_language ==
            project_language
        ):

            return automation


    return None


def validate_test_case_project(
    *,
    project: ProjectDB,
    requirement: RequirementDB,
    scenario: TestScenarioDB,
    test_case: TestCaseDB
) -> None:

    if (
        requirement.project_id !=
        project.id
    ):

        raise TestCycleValidationError(
            "Selected Test Case does not "
            "belong to this Project"
        )


    if (
        scenario.requirement_db_id !=
        requirement.id
    ):

        raise TestCycleValidationError(
            "Scenario and Requirement "
            "traceability is inconsistent"
        )


    if (
        test_case.requirement_db_id !=
        requirement.id
    ):

        raise TestCycleValidationError(
            "Test Case and Requirement "
            "traceability is inconsistent"
        )


    if (
        test_case.test_scenario_db_id !=
        scenario.id
    ):

        raise TestCycleValidationError(
            "Test Case and Scenario "
            "traceability is inconsistent"
        )


def resolve_cycle_test_case_context(
    db: Session,
    *,
    project: ProjectDB,
    test_case_id: int
):

    test_case = (
        db.query(
            TestCaseDB
        )
        .filter(
            TestCaseDB.id ==
            test_case_id
        )
        .first()
    )


    if test_case is None:

        raise TestCycleValidationError(
            "Selected Test Case was "
            "not found"
        )


    review_status = normalise_text(
        test_case.review_status
    )


    if review_status != "approved":

        raise TestCycleValidationError(
            "Only APPROVED Test Cases "
            "can be added to a Test Cycle"
        )


    if (
        test_case.test_scenario_db_id
        is None
    ):

        raise TestCycleValidationError(
            "Selected Test Case is not "
            "linked to a Test Scenario"
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

        raise TestCycleValidationError(
            "Parent Test Scenario "
            "was not found"
        )


    requirement = (
        db.query(
            RequirementDB
        )
        .filter(
            RequirementDB.id ==
            test_case.requirement_db_id
        )
        .first()
    )


    if requirement is None:

        raise TestCycleValidationError(
            "Parent Requirement "
            "was not found"
        )


    validate_test_case_project(
        project=project,
        requirement=requirement,
        scenario=scenario,
        test_case=test_case
    )


    return (
        requirement,
        scenario,
        test_case
    )


def create_test_cycle(
    db: Session,
    *,
    project: ProjectDB,
    request: TestCycleCreate
) -> TestCycleDB:

    if project is None:

        raise TestCycleValidationError(
            "Project was not found"
        )


    if not request.items:

        raise TestCycleValidationError(
            "A Test Cycle must contain "
            "at least one Test Case"
        )


    prepared_items = []


    for position, requested_item in enumerate(
        request.items,
        start=1
    ):

        (
            requirement,
            scenario,
            test_case
        ) = resolve_cycle_test_case_context(
            db,
            project=project,
            test_case_id=(
                requested_item.test_case_id
            )
        )


        execution_type = normalise_text(
            test_case.execution_type,
            "manual"
        ) or "manual"


        execution_mode = normalise_text(
            requested_item.execution_mode
        )


        automation_version = None


        if execution_mode == "manual":

            if execution_type not in {
                "manual",
                "both",
            }:

                raise TestCycleValidationError(
                    f"Test Case "
                    f"'{test_case.test_case_id}' "
                    "is not classified for "
                    "Manual execution"
                )


        elif execution_mode == "automation":

            if execution_type not in {
                "automation",
                "both",
            }:

                raise TestCycleValidationError(
                    f"Test Case "
                    f"'{test_case.test_case_id}' "
                    "is not classified for "
                    "Automation execution"
                )


            automation_version = (
                get_compatible_ready_automation(
                    db,
                    project=project,
                    test_case=test_case
                )
            )


            if automation_version is None:

                raise TestCycleValidationError(
                    f"Test Case "
                    f"'{test_case.test_case_id}' "
                    "does not have a compatible "
                    "READY automation version"
                )


            if not has_persisted_input_schema(
                automation_version
            ):

                raise TestCycleValidationError(
                    f"Test Case "
                    f"'{test_case.test_case_id}' "
                    "has a READY automation "
                    "version, but that version "
                    "does not contain a "
                    "persisted input schema"
                )


        else:

            raise TestCycleValidationError(
                "Cycle execution mode must be "
                "manual or automation"
            )


        prepared_items.append(
            {
                "test_case": test_case,
                "execution_mode":
                    execution_mode,
                "automation_version":
                    automation_version,
                "position": position,
            }
        )


    cycle = TestCycleDB(
        project_id=project.id,
        name=request.name.strip(),
        release=clean_optional_text(
            request.release
        ),
        environment=clean_optional_text(
            request.environment
        ),
        status="draft"
    )


    try:

        db.add(
            cycle
        )

        db.flush()


        for prepared_item in prepared_items:

            automation_version = (
                prepared_item[
                    "automation_version"
                ]
            )


            item = CycleTestItemDB(
                cycle_id=cycle.id,

                test_case_id=(
                    prepared_item[
                        "test_case"
                    ].id
                ),

                execution_mode=(
                    prepared_item[
                        "execution_mode"
                    ]
                ),

                automation_version_id=(
                    automation_version.id
                    if automation_version
                    is not None
                    else None
                ),

                status="not_run",

                position=(
                    prepared_item[
                        "position"
                    ]
                )
            )


            db.add(
                item
            )


        db.commit()


        return get_test_cycle(
            db,
            cycle.id
        )


    except Exception:

        db.rollback()

        raise


def get_test_cycle(
    db: Session,
    cycle_id: int
) -> TestCycleDB | None:

    return (
        db.query(
            TestCycleDB
        )
        .options(
    selectinload(
        TestCycleDB.items
    ).selectinload(
        CycleTestItemDB.test_case
    ),

    selectinload(
        TestCycleDB.items
    ).selectinload(
        CycleTestItemDB.automation_version
    )
)
        .filter(
            TestCycleDB.id ==
            cycle_id
        )
        .first()
    )


def get_project_test_cycles(
    db: Session,
    project_id: int
) -> list[TestCycleDB]:

    return (
        db.query(
            TestCycleDB
        )
        .filter(
            TestCycleDB.project_id ==
            project_id
        )
        .order_by(
            TestCycleDB.created_at.desc(),
            TestCycleDB.id.desc()
        )
        .all()
    )
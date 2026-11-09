from datetime import datetime

from sqlalchemy.orm import Session

from backend.automation_engines import (
    get_automation_engine,
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

from backend.db.test_scenario_model import (
    TestScenarioDB,
)

from backend.models.cycle_execution import (
    AutomatedCycleRunRequest,
)

from backend.services.automation_runtime_input_service import (
    validate_runtime_inputs,
)

from backend.services.cycle_automation_runtime_service import (
    CycleAutomationRuntimeError,
    get_frozen_cycle_automation,
    prepare_automated_cycle_item_inputs,
)

from backend.services.cycle_lifecycle_service import (
    ensure_cycle_in_progress,
)

from backend.services.cycle_manual_result_service import (
    get_item_cycle,
)

from backend.services.execution_runtime_service import (
    build_execution_environment,
)

from backend.services.execution_runner_service import (
    run_execution,
)

from backend.services.execution_service import (
    create_execution,
)


class CycleAutomationExecutionError(
    ValueError
):
    pass


def normalise_text(
    value
) -> str:

    return str(
        value or ""
    ).strip().lower()


def resolve_cycle_execution_context(
    db: Session,
    *,
    cycle_item: CycleTestItemDB
):

    test_case = (
        db.query(
            TestCaseDB
        )
        .filter(
            TestCaseDB.id ==
            cycle_item.test_case_id
        )
        .first()
    )


    if test_case is None:

        raise CycleAutomationExecutionError(
            "Cycle item Test Case "
            "was not found"
        )


    if (
        test_case.test_scenario_db_id
        is None
    ):

        raise CycleAutomationExecutionError(
            "Cycle item Test Case is not "
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

        raise CycleAutomationExecutionError(
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

        raise CycleAutomationExecutionError(
            "Parent Requirement "
            "was not found"
        )


    if (
        scenario.requirement_db_id !=
        requirement.id
    ):

        raise CycleAutomationExecutionError(
            "Scenario and Requirement "
            "traceability is inconsistent"
        )


    if (
        test_case.requirement_db_id !=
        requirement.id
    ):

        raise CycleAutomationExecutionError(
            "Test Case and Requirement "
            "traceability is inconsistent"
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

        raise CycleAutomationExecutionError(
            "Parent Project was not found"
        )


    cycle = get_item_cycle(
        db,
        cycle_item
    )


    if cycle is None:

        raise CycleAutomationExecutionError(
            "Parent Test Cycle "
            "was not found"
        )


    if cycle.project_id != project.id:

        raise CycleAutomationExecutionError(
            "Cycle item Project "
            "traceability is inconsistent"
        )


    return (
        cycle,
        project,
        requirement,
        scenario,
        test_case,
    )


def map_execution_status_to_cycle_item(
    execution_status: str
) -> str:

    status = normalise_text(
        execution_status
    )


    if status in {
        "passed",
        "failed",
        "error",
    }:

        return status


    raise CycleAutomationExecutionError(
        "Automated Execution returned "
        f"an unsupported status: {status}"
    )


def execute_automated_cycle_item(
    db: Session,
    *,
    cycle_item: CycleTestItemDB,
    request: AutomatedCycleRunRequest
) -> CycleTestItemDB:

    if cycle_item is None:

        raise CycleAutomationExecutionError(
            "Cycle Test Item was not found"
        )


    if (
        normalise_text(
            cycle_item.execution_mode
        ) != "automation"
    ):

        raise CycleAutomationExecutionError(
            "Only Automated Cycle Test "
            "Items can use automated "
            "execution"
        )


    (
        cycle,
        project,
        requirement,
        scenario,
        test_case,
    ) = resolve_cycle_execution_context(
        db,
        cycle_item=cycle_item
    )


    ensure_cycle_in_progress(
        cycle
    )


    item_status = normalise_text(
        cycle_item.status
    )


    if item_status != "not_run":

        raise CycleAutomationExecutionError(
            "Automated Cycle Test Item "
            "must be NOT_RUN before execution"
        )


    if cycle_item.execution_id is not None:

        raise CycleAutomationExecutionError(
            "Automated Cycle Test Item "
            "already references an Execution"
        )


    automation = (
        get_frozen_cycle_automation(
            db,
            cycle_item
        )
    )


    if automation is None:

        raise CycleAutomationExecutionError(
            "Frozen automation version "
            "was not found"
        )


    if (
        automation.id !=
        cycle_item.automation_version_id
    ):

        raise CycleAutomationExecutionError(
            "Frozen automation version "
            "does not match the Cycle item"
        )


    if (
        automation.test_case_db_id !=
        test_case.id
    ):

        raise CycleAutomationExecutionError(
            "Frozen automation version "
            "does not belong to the Cycle "
            "item Test Case"
        )


    automation_status = normalise_text(
        automation.status
    )


    if automation_status not in {
        "ready",
        "superseded",
    }:

        raise CycleAutomationExecutionError(
            "Frozen automation version "
            "is not executable"
        )


    automation_engine = normalise_text(
        automation.engine or
        automation.framework
    )


    automation_language = normalise_text(
        automation.language
    )


    project_engine = normalise_text(
        project.automation_engine
    )


    project_language = normalise_text(
        project.automation_language
    )


    if automation_engine != project_engine:

        raise CycleAutomationExecutionError(
            "Frozen automation engine "
            "does not match the Project "
            "automation engine"
        )


    if (
        automation_language !=
        project_language
    ):

        raise CycleAutomationExecutionError(
            "Frozen automation language "
            "does not match the Project "
            "automation language"
        )


    input_schema = (
        prepare_automated_cycle_item_inputs(
            db,
            cycle_item=cycle_item
        )
    )


    try:

        validated_inputs = (
            validate_runtime_inputs(
                input_schema,
                request
            )
        )


    except ValueError as exc:

        raise CycleAutomationExecutionError(
            str(exc)
        ) from exc


    runtime_environment = (
        build_execution_environment(
            validated_inputs
        )
    )


    engine = get_automation_engine(
        project
    )


    engine.validate_source(
        automation.code
    )


    execution = None


    try:

        execution = create_execution(
            db,
            automation.id
        )


        cycle_item.execution_id = (
            execution.id
        )

        cycle_item.status = "running"

        cycle_item.updated_at = (
            datetime.utcnow()
        )


        db.commit()

        db.refresh(
            cycle_item
        )


        completed_execution = (
            run_execution(
                db=db,
                execution=execution,
                automation=automation,
                engine=engine,
                runtime_environment=(
                    runtime_environment
                )
            )
        )


        cycle_item.status = (
            map_execution_status_to_cycle_item(
                completed_execution.status
            )
        )

        cycle_item.updated_at = (
            datetime.utcnow()
        )


        db.commit()

        db.refresh(
            cycle_item
        )


        return cycle_item


    except Exception:

        db.rollback()


        if (
            execution is not None
            and
            cycle_item.id is not None
        ):

            try:

                current_item = (
                    db.query(
                        CycleTestItemDB
                    )
                    .filter(
                        CycleTestItemDB.id ==
                        cycle_item.id
                    )
                    .first()
                )


                if current_item is not None:

                    current_item.execution_id = (
                        execution.id
                    )

                    current_item.status = "error"

                    current_item.updated_at = (
                        datetime.utcnow()
                    )


                    db.commit()


            except Exception:

                db.rollback()


        raise
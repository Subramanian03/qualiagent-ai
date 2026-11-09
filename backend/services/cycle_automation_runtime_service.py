from sqlalchemy.orm import Session

from backend.db.automation_model import (
    AutomationScriptDB,
)

from backend.db.cycle_test_item_model import (
    CycleTestItemDB,
)

from backend.db.test_cycle_model import (
    TestCycleDB,
)

from backend.models.automation_input_schema import (
    AutomationInputSchema,
)

from backend.services.automation_runtime_input_service import (
    get_persisted_input_schema,
)

from backend.services.cycle_lifecycle_service import (
    ensure_cycle_in_progress,
)


class CycleAutomationRuntimeError(
    ValueError
):
    pass


def normalise_text(
    value
) -> str:

    return str(
        value or ""
    ).strip().lower()


def get_automated_cycle_item(
    db: Session,
    cycle_item_id: int
) -> CycleTestItemDB | None:

    return (
        db.query(
            CycleTestItemDB
        )
        .filter(
            CycleTestItemDB.id ==
            cycle_item_id
        )
        .first()
    )


def get_automated_item_cycle(
    db: Session,
    cycle_item: CycleTestItemDB
) -> TestCycleDB | None:

    return (
        db.query(
            TestCycleDB
        )
        .filter(
            TestCycleDB.id ==
            cycle_item.cycle_id
        )
        .first()
    )


def get_frozen_cycle_automation(
    db: Session,
    cycle_item: CycleTestItemDB
) -> AutomationScriptDB | None:

    if (
        cycle_item.automation_version_id
        is None
    ):

        return None


    return (
        db.query(
            AutomationScriptDB
        )
        .filter(
            AutomationScriptDB.id ==
            cycle_item
            .automation_version_id
        )
        .first()
    )


def prepare_automated_cycle_item_inputs(
    db: Session,
    *,
    cycle_item: CycleTestItemDB
) -> AutomationInputSchema:

    if cycle_item is None:

        raise CycleAutomationRuntimeError(
            "Cycle Test Item was not found"
        )


    execution_mode = normalise_text(
        cycle_item.execution_mode
    )


    if execution_mode != "automation":

        raise CycleAutomationRuntimeError(
            "Runtime inputs can only be "
            "prepared for an Automated "
            "Cycle Test Item"
        )


    cycle = get_automated_item_cycle(
        db,
        cycle_item
    )


    if cycle is None:

        raise CycleAutomationRuntimeError(
            "Parent Test Cycle was not found"
        )


    ensure_cycle_in_progress(
        cycle
    )


    item_status = normalise_text(
        cycle_item.status
    )


    if item_status == "running":

        raise CycleAutomationRuntimeError(
            "Automated Cycle Test Item "
            "is already RUNNING"
        )


    if item_status in {
        "passed",
        "failed",
        "error",
        "blocked",
        "skipped",
    }:

        raise CycleAutomationRuntimeError(
            "Automated Cycle Test Item "
            "already has a final result"
        )


    if item_status != "not_run":

        raise CycleAutomationRuntimeError(
            "Automated Cycle Test Item "
            "must be NOT_RUN before runtime "
            "inputs can be prepared"
        )


    if cycle_item.execution_id is not None:

        raise CycleAutomationRuntimeError(
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

        raise CycleAutomationRuntimeError(
            "Frozen automation version "
            "was not found"
        )


    if (
        automation.id !=
        cycle_item.automation_version_id
    ):

        raise CycleAutomationRuntimeError(
            "Frozen automation version "
            "does not match the Cycle item"
        )


    if (
        automation.test_case_db_id !=
        cycle_item.test_case_id
    ):

        raise CycleAutomationRuntimeError(
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

        raise CycleAutomationRuntimeError(
            "Frozen automation version "
            "is not executable"
        )


    if not (
        automation.code and
        automation.code.strip()
    ):

        raise CycleAutomationRuntimeError(
            "Frozen automation version "
            "does not contain source code"
        )


    try:

        return get_persisted_input_schema(
            automation
        )


    except ValueError as exc:

        raise CycleAutomationRuntimeError(
            str(exc)
        ) from exc
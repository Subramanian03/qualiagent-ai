from datetime import datetime

from sqlalchemy.orm import Session

from backend.db.cycle_test_item_model import (
    CycleTestItemDB,
)

from backend.db.test_cycle_model import (
    TestCycleDB,
)

from backend.models.cycle_execution import (
    ManualCycleResultUpdate,
)

from backend.services.cycle_lifecycle_service import (
    ensure_cycle_in_progress,
)


class ManualCycleResultError(
    ValueError
):
    pass


def normalise_text(
    value
) -> str:

    return str(
        value or ""
    ).strip().lower()


def get_cycle_test_item(
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


def get_item_cycle(
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


def update_manual_cycle_result(
    db: Session,
    *,
    cycle_item: CycleTestItemDB,
    request: ManualCycleResultUpdate
) -> CycleTestItemDB:

    if cycle_item is None:

        raise ManualCycleResultError(
            "Cycle Test Item was not found"
        )


    execution_mode = normalise_text(
        cycle_item.execution_mode
    )


    if execution_mode != "manual":

        raise ManualCycleResultError(
            "Only Manual Cycle Test Items "
            "can receive a human-selected "
            "result"
        )


    if (
        cycle_item.automation_version_id
        is not None
    ):

        raise ManualCycleResultError(
            "Manual Cycle Test Item must "
            "not reference an automation "
            "version"
        )


    if cycle_item.execution_id is not None:

        raise ManualCycleResultError(
            "Manual Cycle Test Item must "
            "not reference an automated "
            "Execution"
        )


    cycle = get_item_cycle(
        db,
        cycle_item
    )


    if cycle is None:

        raise ManualCycleResultError(
            "Parent Test Cycle was not found"
        )


        # The lifecycle service prevents
    # results from being recorded while
    # the Cycle is DRAFT, READY,
    # COMPLETED or CANCELLED.
    ensure_cycle_in_progress(
        cycle
    )


    requested_status = normalise_text(
        request.status
    )


    allowed_statuses = {
        "passed",
        "failed",
        "blocked",
        "skipped",
    }


    if requested_status not in (
        allowed_statuses
    ):

        raise ManualCycleResultError(
            "Manual result must be passed, "
            "failed, blocked or skipped"
        )


    cycle_item.status = (
        requested_status
    )

    cycle_item.actual_result = (
        request.actual_result
    )

    cycle_item.comment = (
        request.comment
    )

    cycle_item.defect_reference = (
        request.defect_reference
    )

    cycle_item.updated_at = (
        datetime.utcnow()
    )


    try:

        db.commit()

        db.refresh(
            cycle_item
        )

        return cycle_item


    except Exception:

        db.rollback()

        raise
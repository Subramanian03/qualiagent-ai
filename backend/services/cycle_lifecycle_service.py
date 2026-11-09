from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy.orm import selectinload

from backend.db.cycle_test_item_model import (
    CycleTestItemDB,
)

from backend.db.test_cycle_model import (
    TestCycleDB,
)


class TestCycleLifecycleError(
    ValueError
):
    pass


TERMINAL_ITEM_STATUSES = {
    "passed",
    "failed",
    "blocked",
    "skipped",
    "error",
}


ALLOWED_CYCLE_TRANSITIONS = {
    "draft": {
        "ready",
        "cancelled",
    },

    "ready": {
        "in_progress",
        "cancelled",
    },

    "in_progress": {
        "completed",
        "cancelled",
    },

    "completed": set(),

    "cancelled": set(),
}


def normalise_status(
    value
) -> str:

    return str(
        value or ""
    ).strip().lower()


def get_cycle_for_lifecycle(
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
            )
        )
        .filter(
            TestCycleDB.id ==
            cycle_id
        )
        .first()
    )


def validate_cycle_transition(
    cycle: TestCycleDB,
    requested_status: str
) -> str:

    if cycle is None:

        raise TestCycleLifecycleError(
            "Test Cycle was not found"
        )


    current_status = normalise_status(
        cycle.status
    )


    target_status = normalise_status(
        requested_status
    )


    if current_status not in (
        ALLOWED_CYCLE_TRANSITIONS
    ):

        raise TestCycleLifecycleError(
            "Test Cycle has an invalid "
            f"current status: {current_status}"
        )


    if target_status == current_status:

        raise TestCycleLifecycleError(
            "Test Cycle is already "
            f"{current_status.upper()}"
        )


    allowed_targets = (
        ALLOWED_CYCLE_TRANSITIONS[
            current_status
        ]
    )


    if target_status not in allowed_targets:

        raise TestCycleLifecycleError(
            "Test Cycle cannot transition "
            f"from {current_status.upper()} "
            f"to {target_status.upper()}"
        )


    return target_status


def validate_cycle_ready(
    cycle: TestCycleDB
) -> None:

    items = list(
        cycle.items or []
    )


    if not items:

        raise TestCycleLifecycleError(
            "Test Cycle must contain at "
            "least one Test Case before "
            "it can become READY"
        )


    for item in items:

        execution_mode = normalise_status(
            item.execution_mode
        )


        if execution_mode not in {
            "manual",
            "automation",
        }:

            raise TestCycleLifecycleError(
                "Cycle Test Item has an "
                "invalid execution mode"
            )


        if (
            execution_mode ==
            "manual"
            and
            item.automation_version_id
            is not None
        ):

            raise TestCycleLifecycleError(
                "Manual Cycle Test Item "
                "must not reference an "
                "automation version"
            )


        if (
            execution_mode ==
            "automation"
            and
            item.automation_version_id
            is None
        ):

            raise TestCycleLifecycleError(
                "Automated Cycle Test Item "
                "must reference a frozen "
                "automation version"
            )


        item_status = normalise_status(
            item.status
        )


        if item_status != "not_run":

            raise TestCycleLifecycleError(
                "A DRAFT Test Cycle can "
                "become READY only when all "
                "items are NOT_RUN"
            )


def validate_cycle_start(
    cycle: TestCycleDB
) -> None:

    items = list(
        cycle.items or []
    )


    if not items:

        raise TestCycleLifecycleError(
            "Empty Test Cycle cannot be "
            "started"
        )


    for item in items:

        if (
            normalise_status(
                item.status
            ) != "not_run"
        ):

            raise TestCycleLifecycleError(
                "A READY Test Cycle can "
                "start only when all items "
                "are NOT_RUN"
            )


def validate_cycle_completion(
    cycle: TestCycleDB
) -> None:

    items = list(
        cycle.items or []
    )


    if not items:

        raise TestCycleLifecycleError(
            "Empty Test Cycle cannot be "
            "completed"
        )


    incomplete_items = [
        item
        for item in items
        if normalise_status(
            item.status
        )
        not in TERMINAL_ITEM_STATUSES
    ]


    if incomplete_items:

        raise TestCycleLifecycleError(
            "Test Cycle cannot be completed "
            "while one or more Test Cases "
            "are NOT_RUN or RUNNING"
        )


def transition_test_cycle(
    db: Session,
    *,
    cycle: TestCycleDB,
    requested_status: str
) -> TestCycleDB:

    target_status = (
        validate_cycle_transition(
            cycle,
            requested_status
        )
    )


    now = datetime.utcnow()


    if target_status == "ready":

        validate_cycle_ready(
            cycle
        )


    elif target_status == "in_progress":

        validate_cycle_start(
            cycle
        )

        cycle.started_at = (
            cycle.started_at or
            now
        )


    elif target_status == "completed":

        validate_cycle_completion(
            cycle
        )

        cycle.completed_at = now


    elif target_status == "cancelled":

        if (
            normalise_status(
                cycle.status
            ) == "in_progress"
        ):

            running_items = [
                item
                for item in (
                    cycle.items or []
                )
                if normalise_status(
                    item.status
                ) == "running"
            ]


            if running_items:

                raise TestCycleLifecycleError(
                    "Test Cycle cannot be "
                    "cancelled while an "
                    "automated Test Case "
                    "is RUNNING"
                )


        cycle.completed_at = now


    cycle.status = target_status


    try:

        db.commit()

        db.refresh(
            cycle
        )


        return get_cycle_for_lifecycle(
            db,
            cycle.id
        )


    except Exception:

        db.rollback()

        raise


def ensure_cycle_in_progress(
    cycle: TestCycleDB
) -> None:

    if cycle is None:

        raise TestCycleLifecycleError(
            "Test Cycle was not found"
        )


    status = normalise_status(
        cycle.status
    )


    if status != "in_progress":

        raise TestCycleLifecycleError(
            "Cycle Test Case results can "
            "only be recorded while the "
            "Test Cycle is IN_PROGRESS"
        )


def get_cycle_result_summary(
    cycle: TestCycleDB
) -> dict:

    counts = {
        "total": 0,
        "not_run": 0,
        "running": 0,
        "passed": 0,
        "failed": 0,
        "blocked": 0,
        "skipped": 0,
        "error": 0,
    }


    for item in (
        cycle.items or []
    ):

        counts["total"] += 1


        status = normalise_status(
            item.status
        )


        if status in counts:

            counts[status] += 1


        counts["completed"] = sum(
        counts[status]
        for status in (
            TERMINAL_ITEM_STATUSES
        )
    )


        counts[
        "completion_eligible"
    ] = (
        counts["total"] > 0
        and
        counts["not_run"] == 0
        and
        counts["running"] == 0
    )


    return counts
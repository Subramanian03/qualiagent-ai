from sqlalchemy.orm import Session


from backend.db.cycle_test_item_model import (
    CycleTestItemDB,
)

from backend.db.execution_model import (
    ExecutionDB,
)

from backend.db.test_cycle_model import (
    TestCycleDB,
)

from backend.models.cycle_reporting import (
    AutomationResultSummary,
    CycleReportingFilterOptions,
    CycleResultSummary,
    CycleStatusSummary,
    ExecutionEvidenceSummary,
    ManualResultSummary,
    ProjectCycleQualitySummary,
)

from backend.models.reporting_filters import (
    CycleReportingFilters,
)


TERMINAL_STATUSES = {
    "passed",
    "failed",
    "blocked",
    "skipped",
    "error",
}


def normalise_status(
    value
) -> str:

    return str(
        value or ""
    ).strip().lower()


def normalise_optional_filter(
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


def get_project_cycle_quality_summary(
    db: Session,
    project_id: int,
    filters: (
        CycleReportingFilters |
        None
    ) = None
) -> ProjectCycleQualitySummary:

    filters = (
        filters
        or
        CycleReportingFilters()
    )


    selected_release = (
        normalise_optional_filter(
            filters.release
        )
    )


    selected_environment = (
        normalise_optional_filter(
            filters.environment
        )
    )


    all_cycles = (
        db.query(
            TestCycleDB
        )
        .filter(
            TestCycleDB.project_id ==
            project_id
        )
        .all()
    )


    available_releases = sorted(
        {
            str(
                cycle.release
            ).strip()

            for cycle in all_cycles

            if (
                cycle.release is not None
                and
                str(
                    cycle.release
                ).strip()
            )
        },
        key=str.casefold
    )


    available_environments = sorted(
        {
            str(
                cycle.environment
            ).strip()

            for cycle in all_cycles

            if (
                cycle.environment is not None
                and
                str(
                    cycle.environment
                ).strip()
            )
        },
        key=str.casefold
    )


    cycles = []


    for cycle in all_cycles:

        cycle_status = normalise_status(
            cycle.status
        )


        cycle_release = (
            normalise_optional_filter(
                cycle.release
            )
        )


        cycle_environment = (
            normalise_optional_filter(
                cycle.environment
            )
        )


        if (
            selected_release is not None
            and
            cycle_release !=
            selected_release
        ):

            continue


        if (
            selected_environment is not None
            and
            cycle_environment !=
            selected_environment
        ):

            continue


        if (
            filters.cycle_status is not None
            and
            cycle_status !=
            filters.cycle_status
        ):

            continue


        cycles.append(
            cycle
        )


    cycle_ids = [
        cycle.id
        for cycle in cycles
    ]


    cycle_counts = {
        "total": len(cycles),
        "draft": 0,
        "ready": 0,
        "in_progress": 0,
        "completed": 0,
    }


    for cycle in cycles:

        status = normalise_status(
            cycle.status
        )


        if status in cycle_counts:

            cycle_counts[
                status
            ] += 1


    items = []


    if cycle_ids:

        item_query = (
            db.query(
                CycleTestItemDB
            )
            .filter(
                CycleTestItemDB.cycle_id
                .in_(
                    cycle_ids
                )
            )
        )


        if (
            filters.result_status
            is not None
        ):

            item_query = (
                item_query.filter(
                    CycleTestItemDB.status ==
                    filters.result_status
                )
            )


        if (
            filters.execution_mode
            is not None
        ):

            item_query = (
                item_query.filter(
                    CycleTestItemDB
                    .execution_mode ==
                    filters.execution_mode
                )
            )


        items = item_query.all()


    result_counts = {
        "total": len(items),
        "completed": 0,
        "not_run": 0,
        "running": 0,
        "passed": 0,
        "failed": 0,
        "blocked": 0,
        "skipped": 0,
        "error": 0,
    }


    manual_counts = {
        "total": 0,
        "passed": 0,
        "failed": 0,
        "blocked": 0,
        "skipped": 0,
    }


    automation_counts = {
        "total": 0,
        "passed": 0,
        "failed": 0,
        "error": 0,
    }


    execution_ids = set()


    for item in items:

        status = normalise_status(
            item.status
        )


        execution_mode = (
            normalise_status(
                item.execution_mode
            )
        )


        if status in result_counts:

            result_counts[
                status
            ] += 1


        if status in TERMINAL_STATUSES:

            result_counts[
                "completed"
            ] += 1


        if execution_mode == "manual":

            manual_counts[
                "total"
            ] += 1


            if status in manual_counts:

                manual_counts[
                    status
                ] += 1


        elif execution_mode == "automation":

            automation_counts[
                "total"
            ] += 1


            if status in automation_counts:

                automation_counts[
                    status
                ] += 1


        if item.execution_id is not None:

            execution_ids.add(
                item.execution_id
            )


    completed_count = (
        result_counts[
            "completed"
        ]
    )


    if completed_count > 0:

        pass_rate = round(
            (
                result_counts[
                    "passed"
                ]
                /
                completed_count
            )
            * 100,
            2
        )

    else:

        pass_rate = 0.0


    executions = []


    if execution_ids:

        executions = (
            db.query(
                ExecutionDB
            )
            .filter(
                ExecutionDB.id.in_(
                    execution_ids
                )
            )
            .all()
        )


    screenshot_count = sum(
        1

        for execution in executions

        if (
            execution.screenshot_path
            is not None
            and
            str(
                execution.screenshot_path
            ).strip()
        )
    )


    trace_count = sum(
        1

        for execution in executions

        if (
            execution.trace_path
            is not None
            and
            str(
                execution.trace_path
            ).strip()
        )
    )


    return ProjectCycleQualitySummary(
        project_id=project_id,

        filter_options=(
            CycleReportingFilterOptions(
                releases=(
                    available_releases
                ),

                environments=(
                    available_environments
                ),

                cycle_statuses=[
                    "draft",
                    "ready",
                    "in_progress",
                    "completed",
                ],

                result_statuses=[
                    "not_run",
                    "running",
                    "passed",
                    "failed",
                    "blocked",
                    "skipped",
                    "error",
                ],

                execution_modes=[
                    "manual",
                    "automation",
                ]
            )
        ),

        cycles=CycleStatusSummary(
            **cycle_counts
        ),

        results=CycleResultSummary(
            **result_counts,
            pass_rate=pass_rate
        ),

        manual=ManualResultSummary(
            **manual_counts
        ),

        automation=AutomationResultSummary(
            **automation_counts
        ),

        evidence=ExecutionEvidenceSummary(
            executions=len(
                executions
            ),

            screenshots=(
                screenshot_count
            ),

            traces=(
                trace_count
            )
        )
    )
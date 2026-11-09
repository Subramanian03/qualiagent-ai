from collections import defaultdict

from sqlalchemy.orm import Session


from backend.db.automation_model import (
    AutomationScriptDB,
)

from backend.db.cycle_test_item_model import (
    CycleTestItemDB,
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

from backend.db.test_cycle_model import (
    TestCycleDB,
)

from backend.db.test_scenario_model import (
    TestScenarioDB,
)

from backend.models.cycle_traceability import (
    CycleTraceabilityExecution,
    CycleTraceabilityOccurrence,
    CycleTraceabilityRequirement,
    CycleTraceabilityScenario,
    CycleTraceabilityTestCase,
    ProjectCycleTraceability,
)
from backend.models.reporting_filters import (
    CycleReportingFilters,
)

def clean_text(
    value,
    default: str = ""
) -> str:

    if value is None:
        return default

    return str(
        value
    ).strip()

def clean_optional_filter(
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

def has_path(
    value
) -> bool:

    return bool(
        value is not None
        and
        str(value).strip()
    )


def get_project_cycle_traceability(
    db: Session,
    project_id: int,
    filters: (
        CycleReportingFilters |
        None
    ) = None
) -> ProjectCycleTraceability:

    filters = (
        filters
        or
        CycleReportingFilters()
    )


    selected_release = (
        clean_optional_filter(
            filters.release
        )
    )


    selected_environment = (
        clean_optional_filter(
            filters.environment
        )
    )

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

        raise ValueError(
            "Project not found"
        )


    requirements = (
        db.query(
            RequirementDB
        )
        .filter(
            RequirementDB.project_id ==
            project_id
        )
        .order_by(
            RequirementDB.id.asc()
        )
        .all()
    )


    requirement_ids = [
        requirement.id
        for requirement in requirements
    ]


    scenarios = []


    if requirement_ids:

        scenarios = (
            db.query(
                TestScenarioDB
            )
            .filter(
                TestScenarioDB
                .requirement_db_id
                .in_(
                    requirement_ids
                )
            )
            .order_by(
                TestScenarioDB.id.asc()
            )
            .all()
        )


    scenario_ids = [
        scenario.id
        for scenario in scenarios
    ]


    test_cases = []


    if scenario_ids:

        test_cases = (
            db.query(
                TestCaseDB
            )
            .filter(
                TestCaseDB
                .test_scenario_db_id
                .in_(
                    scenario_ids
                )
            )
            .order_by(
                TestCaseDB.id.asc()
            )
            .all()
        )


    test_case_ids = [
        test_case.id
        for test_case in test_cases
    ]


    all_cycles = (
        db.query(
            TestCycleDB
        )
        .filter(
            TestCycleDB.project_id ==
            project_id
        )
        .order_by(
            TestCycleDB.created_at.asc(),
            TestCycleDB.id.asc()
        )
        .all()
    )


    cycles = []


    for cycle in all_cycles:

        cycle_release = (
            clean_optional_filter(
                cycle.release
            )
        )


        cycle_environment = (
            clean_optional_filter(
                cycle.environment
            )
        )


        cycle_status = clean_text(
            cycle.status
        ).lower()


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
            filters.cycle_status
            is not None
            and
            cycle_status !=
            filters.cycle_status
        ):

            continue


        cycles.append(
            cycle
        )


    cycle_by_id = {
        cycle.id: cycle
        for cycle in cycles
    }


    cycle_ids = list(
        cycle_by_id.keys()
    )


    cycle_items = []


    if (
        cycle_ids
        and
        test_case_ids
    ):

        item_query = (
            db.query(
                CycleTestItemDB
            )
            .filter(
                CycleTestItemDB.cycle_id
                .in_(
                    cycle_ids
                ),

                CycleTestItemDB.test_case_id
                .in_(
                    test_case_ids
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


        cycle_items = (
            item_query
            .order_by(
                CycleTestItemDB.cycle_id
                .asc(),

                CycleTestItemDB.position
                .asc(),

                CycleTestItemDB.id
                .asc()
            )
            .all()
        )

    automation_ids = {
        item.automation_version_id
        for item in cycle_items
        if (
            item.automation_version_id
            is not None
        )
    }


    automation_by_id = {}


    if automation_ids:

        automations = (
            db.query(
                AutomationScriptDB
            )
            .filter(
                AutomationScriptDB.id
                .in_(
                    automation_ids
                )
            )
            .all()
        )


        automation_by_id = {
            automation.id:
                automation
            for automation in automations
        }


    execution_ids = {
        item.execution_id
        for item in cycle_items
        if item.execution_id is not None
    }


    execution_by_id = {}


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


        execution_by_id = {
            execution.id:
                execution
            for execution in executions
        }


    scenarios_by_requirement = (
        defaultdict(list)
    )


    for scenario in scenarios:

        scenarios_by_requirement[
            scenario.requirement_db_id
        ].append(
            scenario
        )


    test_cases_by_scenario = (
        defaultdict(list)
    )


    for test_case in test_cases:

        test_cases_by_scenario[
            test_case.test_scenario_db_id
        ].append(
            test_case
        )


    items_by_test_case = (
        defaultdict(list)
    )


    for item in cycle_items:

        items_by_test_case[
            item.test_case_id
        ].append(
            item
        )


    requirement_results = []


    for requirement in requirements:

        scenario_results = []


        for scenario in (
            scenarios_by_requirement[
                requirement.id
            ]
        ):

            test_case_results = []


            for test_case in (
                test_cases_by_scenario[
                    scenario.id
                ]
            ):

                occurrence_results = []


                for item in (
                    items_by_test_case[
                        test_case.id
                    ]
                ):

                    cycle = (
                        cycle_by_id.get(
                            item.cycle_id
                        )
                    )


                    if cycle is None:
                        continue


                    automation = (
                        automation_by_id.get(
                            item.automation_version_id
                        )
                    )


                    execution = (
                        execution_by_id.get(
                            item.execution_id
                        )
                    )


                    execution_result = None


                    if execution is not None:

                        execution_result = (
                            CycleTraceabilityExecution(
                                id=execution.id,

                                status=clean_text(
                                    execution.status,
                                    "unknown"
                                ),

                                exit_code=(
                                    execution.exit_code
                                ),

                                duration_ms=(
                                    execution.duration_ms
                                ),

                                screenshot_available=(
                                    has_path(
                                        execution
                                        .screenshot_path
                                    )
                                ),

                                trace_available=(
                                    has_path(
                                        execution
                                        .trace_path
                                    )
                                )
                            )
                        )


                    occurrence_results.append(
                        CycleTraceabilityOccurrence(
                            cycle_id=cycle.id,

                            cycle_name=clean_text(
                                cycle.name,
                                (
                                    f"Cycle "
                                    f"{cycle.id}"
                                )
                            ),

                            cycle_status=(
                                clean_text(
                                    cycle.status,
                                    "unknown"
                                )
                            ),

                            release=(
                                cycle.release
                            ),

                            environment=(
                                cycle.environment
                            ),

                            cycle_item_id=item.id,

                            position=item.position,

                            execution_mode=(
                                clean_text(
                                    item.execution_mode,
                                    "unknown"
                                )
                            ),

                            result_status=(
                                clean_text(
                                    item.status,
                                    "not_run"
                                )
                            ),

                            actual_result=(
                                item.actual_result
                            ),

                            comment=(
                                item.comment
                            ),

                            defect_reference=(
                                item.defect_reference
                            ),

                            automation_version_id=(
                                item
                                .automation_version_id
                            ),

                            automation_version_number=(
                                automation.version
                                if automation
                                is not None
                                else None
                            ),

                            automation_engine=(
                                (
                                    automation.engine
                                    or
                                    automation.framework
                                )
                                if automation
                                is not None
                                else None
                            ),

                            automation_language=(
                                automation.language
                                if automation
                                is not None
                                else None
                            ),

                            execution=(
                                execution_result
                            ),

                            cycle_started_at=(
                                cycle.started_at
                            ),

                            cycle_completed_at=(
                                cycle.completed_at
                            )
                        )
                    )


                test_case_results.append(
                    CycleTraceabilityTestCase(
                        id=test_case.id,

                        test_case_id=(
                            clean_text(
                                test_case
                                .test_case_id,

                                str(
                                    test_case.id
                                )
                            )
                        ),

                        title=clean_text(
                            test_case.title,
                            "Untitled Test Case"
                        ),

                        test_type=(
                            test_case.test_type
                        ),

                        priority=(
                            test_case.priority
                        ),

                        current_execution_type=(
                            test_case
                            .execution_type
                        ),

                        occurrences=(
                            occurrence_results
                        )
                    )
                )


            scenario_results.append(
                CycleTraceabilityScenario(
                    id=scenario.id,

                    scenario_id=clean_text(
                        scenario.scenario_id,
                        str(
                            scenario.id
                        )
                    ),

                    title=clean_text(
                        scenario.title,
                        "Untitled Scenario"
                    ),

                    test_cases=(
                        test_case_results
                    )
                )
            )


        requirement_results.append(
            CycleTraceabilityRequirement(
                id=requirement.id,

                requirement_id=clean_text(
                    requirement.requirement_id,
                    str(
                        requirement.id
                    )
                ),

                title=clean_text(
                    requirement.title,
                    "Untitled Requirement"
                ),

                scenarios=(
                    scenario_results
                )
            )
        )


    return ProjectCycleTraceability(
        project_id=project.id,

        project_name=clean_text(
            project.name,
            f"Project {project.id}"
        ),

        requirements=(
            requirement_results
        )
    )
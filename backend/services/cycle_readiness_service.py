from sqlalchemy.orm import Session

from backend.db.automation_model import (
    AutomationScriptDB,
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

from backend.models.cycle_readiness import (
    CycleReadyRequirement,
    CycleReadyScenario,
    CycleReadyTestCase,
    ProjectCycleReadiness,
    ReadyAutomationSummary,
)

from backend.services.test_cycle_service import (
    has_persisted_input_schema,
)


def normalise_text(
    value,
    default: str = ""
) -> str:

    return str(
        value
        if value is not None
        else default
    ).strip().lower()


def get_project_cycle_readiness(
    db: Session,
    project: ProjectDB
) -> ProjectCycleReadiness:

    if project is None:

        raise ValueError(
            "Project was not found"
        )


    project_engine = normalise_text(
        project.automation_engine
    )


    project_language = normalise_text(
        project.automation_language
    )


    requirements = (
        db.query(
            RequirementDB
        )
        .filter(
            RequirementDB.project_id ==
            project.id
        )
        .order_by(
            RequirementDB.id.asc()
        )
        .all()
    )


    if not requirements:

        return ProjectCycleReadiness(
            project_id=project.id,
            project_name=project.name,
            requirements=[]
        )


    requirement_ids = [
        requirement.id
        for requirement in requirements
    ]


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


    scenarios_by_requirement = {
        requirement_id: []
        for requirement_id
        in requirement_ids
    }


    for scenario in scenarios:

        scenarios_by_requirement.setdefault(
            scenario.requirement_db_id,
            []
        ).append(
            scenario
        )


    scenario_ids = [
        scenario.id
        for scenario in scenarios
    ]


    if not scenario_ids:

        return ProjectCycleReadiness(
            project_id=project.id,
            project_name=project.name,
            requirements=[]
        )


    test_cases = (
        db.query(
            TestCaseDB
        )
        .filter(
            TestCaseDB
            .test_scenario_db_id
            .in_(
                scenario_ids
            ),
            TestCaseDB.review_status ==
            "approved"
        )
        .order_by(
            TestCaseDB.id.asc()
        )
        .all()
    )


    test_cases_by_scenario = {
        scenario_id: []
        for scenario_id
        in scenario_ids
    }


    for test_case in test_cases:

        test_cases_by_scenario.setdefault(
            test_case.test_scenario_db_id,
            []
        ).append(
            test_case
        )


    test_case_ids = [
        test_case.id
        for test_case in test_cases
    ]


    ready_automation_by_test_case = {}


    if test_case_ids:

        ready_automations = (
            db.query(
                AutomationScriptDB
            )
            .filter(
                AutomationScriptDB
                .test_case_db_id
                .in_(
                    test_case_ids
                ),
                AutomationScriptDB.status ==
                "ready"
            )
            .order_by(
                AutomationScriptDB
                .test_case_db_id
                .asc(),
                AutomationScriptDB
                .version
                .desc(),
                AutomationScriptDB
                .id
                .desc()
            )
            .all()
        )


        for automation in ready_automations:

            test_case_id = (
                automation
                .test_case_db_id
            )


            if (
                test_case_id
                in
                ready_automation_by_test_case
            ):

                continue


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


                        # Only automation matching the
            # current Project engine and
            # language can be frozen into a
            # future automated Cycle item.
            if (
                automation_engine !=
                project_engine
                or
                automation_language !=
                project_language
            ):

                continue


            ready_automation_by_test_case[
                test_case_id
            ] = automation


    requirement_responses = []


    for requirement in requirements:

        scenario_responses = []


        for scenario in (
            scenarios_by_requirement.get(
                requirement.id,
                []
            )
        ):

            test_case_responses = []


            for test_case in (
                test_cases_by_scenario.get(
                    scenario.id,
                    []
                )
            ):

                execution_type = (
                    normalise_text(
                        test_case.execution_type,
                        "manual"
                    )
                    or
                    "manual"
                )


                manual_eligible = (
                    execution_type
                    in {
                        "manual",
                        "both",
                    }
                )


                ready_automation = (
                    ready_automation_by_test_case
                    .get(
                        test_case.id
                    )
                )


                automation_eligible = (
    execution_type
    in {
        "automation",
        "both",
    }
    and
    ready_automation
    is not None
    and
    has_persisted_input_schema(
        ready_automation
    )
)


                ready_summary = None


                if ready_automation is not None:

                    ready_summary = (
                        ReadyAutomationSummary(
                            id=(
                                ready_automation.id
                            ),
                            version=(
                                ready_automation
                                .version
                            ),
                            engine=(
                                normalise_text(
                                    ready_automation
                                    .engine
                                    or
                                    ready_automation
                                    .framework
                                )
                            ),
                            language=(
                                normalise_text(
                                    ready_automation
                                    .language
                                )
                            ),
                            status="ready"
                        )
                    )


                test_case_responses.append(
                    CycleReadyTestCase(
                        id=test_case.id,
                        test_case_id=(
                            test_case
                            .test_case_id
                        ),
                        title=(
                            test_case.title
                        ),
                        test_type=(
                            test_case.test_type
                        ),
                        priority=(
                            test_case.priority
                        ),
                        automation_candidate=(
                            bool(
                                test_case
                                .automation_candidate
                            )
                        ),
                        execution_type=(
                            execution_type
                        ),
                        manual_eligible=(
                            manual_eligible
                        ),
                        automation_eligible=(
                            automation_eligible
                        ),
                        ready_automation=(
                            ready_summary
                        )
                    )
                )


                        # Exclude Scenarios that have no
            # approved Test Cases.
            if not test_case_responses:

                continue


            scenario_responses.append(
                CycleReadyScenario(
                    id=scenario.id,
                    scenario_id=(
                        scenario.scenario_id
                    ),
                    title=scenario.title,
                    test_cases=(
                        test_case_responses
                    )
                )
            )


                # Exclude Requirements that have no
        # approved Test Cases.
        if not scenario_responses:

            continue


        requirement_responses.append(
            CycleReadyRequirement(
                id=requirement.id,
                requirement_id=(
                    requirement
                    .requirement_id
                ),
                title=requirement.title,
                scenarios=(
                    scenario_responses
                )
            )
        )


    return ProjectCycleReadiness(
        project_id=project.id,
        project_name=project.name,
        requirements=(
            requirement_responses
        )
    )
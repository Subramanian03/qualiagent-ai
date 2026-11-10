from sqlalchemy.orm import Session


from backend.models.release_quality import (
    ProjectReleaseQuality,
    ReleaseEvidenceSummary,
    ReleaseExecutionModeSummary,
    ReleaseExecutionSummary,
    ReleaseReadinessReason,
    ReleaseRiskExecution,
    ReleaseRiskItem,
)

from backend.models.reporting_filters import (
    CycleReportingFilters,
)

from backend.services.cycle_reporting_service import (
    get_project_cycle_quality_summary,
)

from backend.services.cycle_traceability_service import (
    get_project_cycle_traceability,
)


READY_PASS_RATE = 90.0


RELEASE_RISK_RULES = {
    "not_run": {
        "severity": "blocker",
        "risk_code": "NOT_RUN",
    },

    "running": {
        "severity": "blocker",
        "risk_code": "RUNNING",
    },

    "blocked": {
        "severity": "blocker",
        "risk_code": "BLOCKED",
    },

    "error": {
        "severity": "blocker",
        "risk_code": "ERROR",
    },

    "failed": {
        "severity": "high",
        "risk_code": "FAILED_TEST",
    },
}


def clean_required_text(
    value,
    field_name: str
) -> str:

    cleaned = str(
        value or ""
    ).strip()


    if not cleaned:

        raise ValueError(
            f"{field_name} is required"
        )


    return cleaned


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


def build_release_risks(
    traceability
) -> list:

    risks = []


    for requirement in (
        traceability.requirements
    ):

        for scenario in (
            requirement.scenarios
        ):

            for test_case in (
                scenario.test_cases
            ):

                for occurrence in (
                    test_case.occurrences
                ):

                    result_status = str(
                        occurrence.result_status
                        or
                        ""
                    ).strip().lower()


                    rule = (
                        RELEASE_RISK_RULES
                        .get(
                            result_status
                        )
                    )


                    if rule is None:

                        continue


                    execution_result = None


                    if (
                        occurrence.execution
                        is not None
                    ):

                        execution = (
                            occurrence.execution
                        )


                        execution_result = (
                            ReleaseRiskExecution(
                                id=(
                                    execution.id
                                ),

                                status=str(
                                    execution.status
                                    or
                                    "unknown"
                                ).strip().lower(),

                                exit_code=(
                                    execution.exit_code
                                ),

                                duration_ms=(
                                    execution.duration_ms
                                ),

                                screenshot_available=(
                                    execution
                                    .screenshot_available
                                ),

                                trace_available=(
                                    execution
                                    .trace_available
                                )
                            )
                        )


                    risks.append(
                        ReleaseRiskItem(
                            severity=(
                                rule[
                                    "severity"
                                ]
                            ),

                            risk_code=(
                                rule[
                                    "risk_code"
                                ]
                            ),

                            requirement_id=(
                                requirement
                                .requirement_id
                            ),

                            requirement_title=(
                                requirement.title
                            ),

                            scenario_id=(
                                scenario.scenario_id
                            ),

                            scenario_title=(
                                scenario.title
                            ),

                            test_case_db_id=(
                                test_case.id
                            ),

                            test_case_id=(
                                test_case
                                .test_case_id
                            ),

                            test_case_title=(
                                test_case.title
                            ),

                            cycle_id=(
                                occurrence.cycle_id
                            ),

                            cycle_name=(
                                occurrence.cycle_name
                            ),

                            cycle_status=(
                                occurrence
                                .cycle_status
                            ),

                            release=(
                                occurrence.release
                            ),

                            environment=(
                                occurrence.environment
                            ),

                            execution_mode=(
                                occurrence
                                .execution_mode
                            ),

                            result_status=(
                                result_status
                            ),

                            automation_version_id=(
                                occurrence
                                .automation_version_id
                            ),

                            automation_version_number=(
                                occurrence
                                .automation_version_number
                            ),

                            automation_engine=(
                                occurrence
                                .automation_engine
                            ),

                            automation_language=(
                                occurrence
                                .automation_language
                            ),

                            execution=(
                                execution_result
                            )
                        )
                    )


    severity_order = {
        "blocker": 0,
        "high": 1,
    }


    risks.sort(
        key=lambda risk: (
            severity_order.get(
                risk.severity,
                99
            ),
            risk.requirement_id,
            risk.scenario_id,
            risk.test_case_id,
            risk.cycle_id,
        )
    )


    return risks

def determine_release_signal(
    *,
    planned_tests: int,
    completed_tests: int,
    not_run: int,
    running: int,
    failed: int,
    blocked: int,
    error: int,
    pass_rate: float
) -> tuple[
    str,
    list[ReleaseReadinessReason]
]:

    reasons = []


    if planned_tests == 0:

        reasons.append(
            ReleaseReadinessReason(
                code="NO_TESTS",

                message=(
                    "No Test Cases are planned "
                    "for the selected Release "
                    "and Environment."
                )
            )
        )


        return (
            "not_ready",
            reasons
        )


    if not_run > 0:

        reasons.append(
            ReleaseReadinessReason(
                code="NOT_RUN",

                message=(
                    f"{not_run} planned Test "
                    "Case(s) have not been run."
                )
            )
        )


    if running > 0:

        reasons.append(
            ReleaseReadinessReason(
                code="RUNNING",

                message=(
                    f"{running} Test Case(s) "
                    "are still running."
                )
            )
        )


    if blocked > 0:

        reasons.append(
            ReleaseReadinessReason(
                code="BLOCKED",

                message=(
                    f"{blocked} Test Case(s) "
                    "are blocked."
                )
            )
        )


    if error > 0:

        reasons.append(
            ReleaseReadinessReason(
                code="ERROR",

                message=(
                    f"{error} automated Test "
                    "Case(s) ended with an "
                    "execution error."
                )
            )
        )


    hard_gate_codes = {
        "NO_TESTS",
        "NOT_RUN",
        "RUNNING",
        "BLOCKED",
        "ERROR",
    }


    if any(
        reason.code in hard_gate_codes
        for reason in reasons
    ):

        return (
            "not_ready",
            reasons
        )


    if completed_tests == 0:

        reasons.append(
            ReleaseReadinessReason(
                code="NO_COMPLETED_TESTS",

                message=(
                    "No Test Cases have a "
                    "completed result."
                )
            )
        )


        return (
            "not_ready",
            reasons
        )


    if failed > 0:

        reasons.append(
            ReleaseReadinessReason(
                code="FAILED_TESTS",

                message=(
                    f"{failed} completed Test "
                    "Case(s) failed."
                )
            )
        )


    if pass_rate < READY_PASS_RATE:

        reasons.append(
            ReleaseReadinessReason(
                code="PASS_RATE",

                message=(
                    f"Pass rate {pass_rate}% "
                    "is below the "
                    f"{READY_PASS_RATE}% "
                    "release-readiness threshold."
                )
            )
        )


    if reasons:

        return (
            "at_risk",
            reasons
        )


    reasons.append(
        ReleaseReadinessReason(
            code="READY",

            message=(
                "All planned Test Cases have "
                "completed without failed, "
                "blocked, or error results, "
                "and the pass rate satisfies "
                "the release-readiness threshold."
            )
        )
    )


    return (
        "ready",
        reasons
    )


def get_project_release_quality(
    db: Session,
    *,
    project_id: int,
    release: str,
    environment: str | None = None
) -> ProjectReleaseQuality:

    selected_release = (
        clean_required_text(
            release,
            "Release"
        )
    )


    selected_environment = (
        clean_optional_text(
            environment
        )
    )


    reporting_filters = (
        CycleReportingFilters(
            release=(
                selected_release
            ),

            environment=(
                selected_environment
            )
        )
    )


    summary = (
        get_project_cycle_quality_summary(
            db,
            project_id,
            reporting_filters
        )
    )


    traceability = (
        get_project_cycle_traceability(
            db,
            project_id,
            reporting_filters
        )
    )


    risks = (
        build_release_risks(
            traceability
        )
    )


    signal, reasons = (
        determine_release_signal(
            planned_tests=(
                summary.results.total
            ),

            completed_tests=(
                summary.results.completed
            ),

            not_run=(
                summary.results.not_run
            ),

            running=(
                summary.results.running
            ),

            failed=(
                summary.results.failed
            ),

            blocked=(
                summary.results.blocked
            ),

            error=(
                summary.results.error
            ),

            pass_rate=(
                summary.results.pass_rate
            )
        )
    )


    return ProjectReleaseQuality(
        project_id=project_id,

        release=(
            selected_release
        ),

        environment=(
            selected_environment
        ),

        signal=(
            signal
        ),

        execution=(
            ReleaseExecutionSummary(
                cycles=(
                    summary.cycles.total
                ),

                completed_cycles=(
                    summary.cycles.completed
                ),

                planned_tests=(
                    summary.results.total
                ),

                completed_tests=(
                    summary.results.completed
                ),

                not_run=(
                    summary.results.not_run
                ),

                running=(
                    summary.results.running
                ),

                passed=(
                    summary.results.passed
                ),

                failed=(
                    summary.results.failed
                ),

                blocked=(
                    summary.results.blocked
                ),

                skipped=(
                    summary.results.skipped
                ),

                error=(
                    summary.results.error
                ),

                pass_rate=(
                    summary.results.pass_rate
                )
            )
        ),

        execution_modes=(
            ReleaseExecutionModeSummary(
                manual_total=(
                    summary.manual.total
                ),

                manual_passed=(
                    summary.manual.passed
                ),

                manual_failed=(
                    summary.manual.failed
                ),

                manual_blocked=(
                    summary.manual.blocked
                ),

                manual_skipped=(
                    summary.manual.skipped
                ),

                automation_total=(
                    summary.automation.total
                ),

                automation_passed=(
                    summary.automation.passed
                ),

                automation_failed=(
                    summary.automation.failed
                ),

                automation_error=(
                    summary.automation.error
                )
            )
        ),

        evidence=(
            ReleaseEvidenceSummary(
                executions=(
                    summary.evidence.executions
                ),

                screenshots=(
                    summary.evidence.screenshots
                ),

                traces=(
                    summary.evidence.traces
                )
            )
        ),

        reasons=(
            reasons
        ),

        risks=(
            risks
        )
    )
from sqlalchemy.orm import Session


from backend.models.release_quality import (
    ProjectReleaseQuality,
    ReleaseEvidenceSummary,
    ReleaseExecutionModeSummary,
    ReleaseExecutionSummary,
    ReleaseReadinessReason,
)

from backend.models.reporting_filters import (
    CycleReportingFilters,
)

from backend.services.cycle_reporting_service import (
    get_project_cycle_quality_summary,
)


READY_PASS_RATE = 90.0


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
                    f"is below the "
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


    summary = (
        get_project_cycle_quality_summary(
            db,
            project_id,
            CycleReportingFilters(
                release=(
                    selected_release
                ),
                environment=(
                    selected_environment
                )
            )
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

        release=selected_release,

        environment=(
            selected_environment
        ),

        signal=signal,

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

        reasons=reasons
    )
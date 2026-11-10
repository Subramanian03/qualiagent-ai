from io import BytesIO

from openpyxl import Workbook
from openpyxl.styles import Alignment
from openpyxl.styles import Border
from openpyxl.styles import Font
from openpyxl.styles import PatternFill
from openpyxl.styles import Side
from openpyxl.utils import get_column_letter


HEADER_FILL = PatternFill(
    fill_type="solid",
    fgColor="1F4E78"
)

SECTION_FILL = PatternFill(
    fill_type="solid",
    fgColor="D9EAF7"
)

READY_FILL = PatternFill(
    fill_type="solid",
    fgColor="DCFCE7"
)

AT_RISK_FILL = PatternFill(
    fill_type="solid",
    fgColor="FEF3C7"
)

NOT_READY_FILL = PatternFill(
    fill_type="solid",
    fgColor="FEE2E2"
)

BLOCKER_FILL = PatternFill(
    fill_type="solid",
    fgColor="FEE2E2"
)

HIGH_FILL = PatternFill(
    fill_type="solid",
    fgColor="FEF3C7"
)

WHITE_FONT = Font(
    color="FFFFFF",
    bold=True
)

BOLD_FONT = Font(
    bold=True
)

THIN_SIDE = Side(
    style="thin",
    color="D0D5DD"
)

CELL_BORDER = Border(
    left=THIN_SIDE,
    right=THIN_SIDE,
    top=THIN_SIDE,
    bottom=THIN_SIDE
)


def clean_text(
    value,
    default: str = ""
) -> str:

    if value is None:
        return default


    cleaned = str(
        value
    ).strip()


    return (
        cleaned
        if cleaned
        else default
    )


def display_status(
    value,
    default: str = "UNKNOWN"
) -> str:

    return (
        clean_text(
            value,
            default
        )
        .replace(
            "_",
            " "
        )
        .upper()
    )


def set_sheet_title(
    worksheet,
    title: str,
    subtitle: str | None = None
):

    worksheet.merge_cells(
        "A1:F1"
    )

    worksheet[
        "A1"
    ] = title

    worksheet[
        "A1"
    ].font = Font(
        bold=True,
        color="FFFFFF",
        size=16
    )

    worksheet[
        "A1"
    ].fill = HEADER_FILL

    worksheet[
        "A1"
    ].alignment = Alignment(
        horizontal="left",
        vertical="center"
    )

    worksheet.row_dimensions[
        1
    ].height = 26


    if subtitle:

        worksheet.merge_cells(
            "A2:F2"
        )

        worksheet[
            "A2"
        ] = subtitle

        worksheet[
            "A2"
        ].font = Font(
            italic=True,
            color="475467"
        )

        worksheet[
            "A2"
        ].alignment = Alignment(
            wrap_text=True
        )


def style_header_row(
    worksheet,
    row_number: int
):

    for cell in worksheet[
        row_number
    ]:

        cell.fill = HEADER_FILL
        cell.font = WHITE_FONT
        cell.alignment = Alignment(
            horizontal="center",
            vertical="center",
            wrap_text=True
        )
        cell.border = CELL_BORDER


def style_data_area(
    worksheet,
    min_row: int,
    max_row: int,
    min_column: int,
    max_column: int
):

    if max_row < min_row:
        return


    for row in worksheet.iter_rows(
        min_row=min_row,
        max_row=max_row,
        min_col=min_column,
        max_col=max_column
    ):

        for cell in row:

            cell.border = CELL_BORDER

            cell.alignment = Alignment(
                vertical="top",
                wrap_text=True
            )


def set_column_widths(
    worksheet,
    widths: dict
):

    for column, width in widths.items():

        worksheet.column_dimensions[
            column
        ].width = width


def add_summary_sheet(
    workbook,
    project_name: str,
    release_quality
):

    worksheet = workbook.active

    worksheet.title = "Summary"


    set_sheet_title(
        worksheet,
        "QualiAgent Release Quality Report",
        (
            f"Project: {project_name} | "
            f"Release: {release_quality.release} | "
            "Environment: "
            f"{release_quality.environment or 'All Environments'}"
        )
    )


    signal = clean_text(
        release_quality.signal,
        "unknown"
    ).lower()


    worksheet[
        "A4"
    ] = "Release Signal"

    worksheet[
        "B4"
    ] = display_status(
        signal
    )

    worksheet[
        "A4"
    ].font = BOLD_FONT

    worksheet[
        "B4"
    ].font = Font(
        bold=True,
        size=14
    )


    if signal == "ready":

        worksheet[
            "B4"
        ].fill = READY_FILL

    elif signal == "at_risk":

        worksheet[
            "B4"
        ].fill = AT_RISK_FILL

    else:

        worksheet[
            "B4"
        ].fill = NOT_READY_FILL


    execution = (
        release_quality.execution
    )


    summary_rows = [
        (
            "Project",
            project_name
        ),
        (
            "Release",
            release_quality.release
        ),
        (
            "Environment",
            (
                release_quality.environment
                or
                "All Environments"
            )
        ),
        (
            "Test Cycles",
            execution.cycles
        ),
        (
            "Completed Cycles",
            execution.completed_cycles
        ),
        (
            "Planned Tests",
            execution.planned_tests
        ),
        (
            "Completed Tests",
            execution.completed_tests
        ),
        (
            "Passed",
            execution.passed
        ),
        (
            "Failed",
            execution.failed
        ),
        (
            "Blocked",
            execution.blocked
        ),
        (
            "Skipped",
            execution.skipped
        ),
        (
            "Not Run",
            execution.not_run
        ),
        (
            "Running",
            execution.running
        ),
        (
            "Errors",
            execution.error
        ),
        (
            "Pass Rate",
            execution.pass_rate / 100
        ),
        (
            "Executions",
            release_quality.evidence.executions
        ),
        (
            "Screenshots",
            release_quality.evidence.screenshots
        ),
        (
            "Traces",
            release_quality.evidence.traces
        ),
    ]


    worksheet[
        "A6"
    ] = "Metric"

    worksheet[
        "B6"
    ] = "Value"

    style_header_row(
        worksheet,
        6
    )


    for row_number, (
        label,
        value
    ) in enumerate(
        summary_rows,
        start=7
    ):

        worksheet.cell(
            row=row_number,
            column=1,
            value=label
        )

        worksheet.cell(
            row=row_number,
            column=2,
            value=value
        )


        worksheet.cell(
            row=row_number,
            column=1
        ).font = BOLD_FONT


    pass_rate_row = (
        7 +
        summary_rows.index(
            (
                "Pass Rate",
                execution.pass_rate / 100
            )
        )
    )


    worksheet.cell(
        row=pass_rate_row,
        column=2
    ).number_format = "0.00%"


    style_data_area(
        worksheet,
        7,
        6 + len(
            summary_rows
        ),
        1,
        2
    )


    mode_start = (
        8 +
        len(
            summary_rows
        )
    )


    worksheet.cell(
        row=mode_start,
        column=1,
        value="Execution Mode"
    )

    worksheet.cell(
        row=mode_start,
        column=2,
        value="Total"
    )

    worksheet.cell(
        row=mode_start,
        column=3,
        value="Passed"
    )

    worksheet.cell(
        row=mode_start,
        column=4,
        value="Failed"
    )

    worksheet.cell(
        row=mode_start,
        column=5,
        value="Blocked"
    )

    worksheet.cell(
        row=mode_start,
        column=6,
        value="Skipped / Error"
    )


    style_header_row(
        worksheet,
        mode_start
    )


    modes = (
        release_quality.execution_modes
    )


    worksheet.append(
        [
            "Manual",
            modes.manual_total,
            modes.manual_passed,
            modes.manual_failed,
            modes.manual_blocked,
            modes.manual_skipped,
        ]
    )


    worksheet.append(
        [
            "Automation",
            modes.automation_total,
            modes.automation_passed,
            modes.automation_failed,
            None,
            modes.automation_error,
        ]
    )


    style_data_area(
        worksheet,
        mode_start + 1,
        mode_start + 2,
        1,
        6
    )


    worksheet.freeze_panes = "A6"

    worksheet.auto_filter.ref = (
        f"A6:B{6 + len(summary_rows)}"
    )


    set_column_widths(
        worksheet,
        {
            "A": 28,
            "B": 24,
            "C": 16,
            "D": 16,
            "E": 16,
            "F": 20,
        }
    )


def add_reasons_sheet(
    workbook,
    release_quality
):

    worksheet = workbook.create_sheet(
        "Readiness Reasons"
    )


    set_sheet_title(
        worksheet,
        "Release Readiness Reasons"
    )


    worksheet.append(
        []
    )

    worksheet.append(
        [
            "Code",
            "Message",
        ]
    )


    header_row = 3


    style_header_row(
        worksheet,
        header_row
    )


    reasons = (
        release_quality.reasons
        or
        []
    )


    if reasons:

        for reason in reasons:

            worksheet.append(
                [
                    reason.code,
                    reason.message,
                ]
            )

    else:

        worksheet.append(
            [
                "NONE",
                (
                    "No readiness reasons "
                    "were returned."
                ),
            ]
        )


    style_data_area(
        worksheet,
        header_row + 1,
        worksheet.max_row,
        1,
        2
    )


    worksheet.freeze_panes = "A4"

    worksheet.auto_filter.ref = (
        f"A3:B{worksheet.max_row}"
    )


    set_column_widths(
        worksheet,
        {
            "A": 24,
            "B": 90,
        }
    )


def add_risks_sheet(
    workbook,
    release_quality
):

    worksheet = workbook.create_sheet(
        "Release Risks"
    )


    set_sheet_title(
        worksheet,
        "Release Risks"
    )


    worksheet.append(
        []
    )


    headers = [
        "Severity",
        "Risk Code",
        "Requirement ID",
        "Requirement Title",
        "Scenario ID",
        "Scenario Title",
        "Test Case ID",
        "Test Case Title",
        "Cycle ID",
        "Cycle Name",
        "Cycle Status",
        "Release",
        "Environment",
        "Execution Mode",
        "Result",
        "Automation ID",
        "Automation Version",
        "Automation Engine",
        "Automation Language",
        "Execution ID",
        "Execution Status",
        "Exit Code",
        "Duration (ms)",
        "Screenshot Available",
        "Trace Available",
    ]


    worksheet.append(
        headers
    )


    header_row = 3


    style_header_row(
        worksheet,
        header_row
    )


    risks = (
        release_quality.risks
        or
        []
    )


    for risk in risks:

        execution = (
            risk.execution
        )


        worksheet.append(
            [
                display_status(
                    risk.severity
                ),
                risk.risk_code,
                risk.requirement_id,
                risk.requirement_title,
                risk.scenario_id,
                risk.scenario_title,
                risk.test_case_id,
                risk.test_case_title,
                risk.cycle_id,
                risk.cycle_name,
                display_status(
                    risk.cycle_status
                ),
                risk.release,
                risk.environment,
                display_status(
                    risk.execution_mode
                ),
                display_status(
                    risk.result_status
                ),
                risk.automation_version_id,
                risk.automation_version_number,
                risk.automation_engine,
                risk.automation_language,
                (
                    execution.id
                    if execution
                    else None
                ),
                (
                    display_status(
                        execution.status
                    )
                    if execution
                    else None
                ),
                (
                    execution.exit_code
                    if execution
                    else None
                ),
                (
                    execution.duration_ms
                    if execution
                    else None
                ),
                (
                    execution
                    .screenshot_available
                    if execution
                    else False
                ),
                (
                    execution.trace_available
                    if execution
                    else False
                ),
            ]
        )


    if not risks:

        worksheet.append(
            [
                "NONE",
                "No Release Risks",
            ]
        )


    style_data_area(
        worksheet,
        header_row + 1,
        worksheet.max_row,
        1,
        len(
            headers
        )
    )


    for row_number in range(
        header_row + 1,
        worksheet.max_row + 1
    ):

        severity = clean_text(
            worksheet.cell(
                row=row_number,
                column=1
            ).value
        ).lower()


        if severity == "blocker":

            worksheet.cell(
                row=row_number,
                column=1
            ).fill = BLOCKER_FILL

        elif severity == "high":

            worksheet.cell(
                row=row_number,
                column=1
            ).fill = HIGH_FILL


    worksheet.freeze_panes = "A4"

    worksheet.auto_filter.ref = (
        f"A3:Y{worksheet.max_row}"
    )


    set_column_widths(
        worksheet,
        {
            "A": 12,
            "B": 18,
            "C": 24,
            "D": 36,
            "E": 26,
            "F": 36,
            "G": 32,
            "H": 48,
            "I": 12,
            "J": 28,
            "K": 18,
            "L": 16,
            "M": 16,
            "N": 18,
            "O": 16,
            "P": 16,
            "Q": 18,
            "R": 18,
            "S": 20,
            "T": 15,
            "U": 18,
            "V": 12,
            "W": 16,
            "X": 22,
            "Y": 18,
        }
    )


def add_traceability_sheet(
    workbook,
    traceability
):

    worksheet = workbook.create_sheet(
        "Traceability"
    )


    set_sheet_title(
        worksheet,
        "Requirement to Execution Traceability"
    )


    worksheet.append(
        []
    )


    headers = [
        "Requirement ID",
        "Requirement Title",
        "Scenario ID",
        "Scenario Title",
        "Test Case ID",
        "Test Case Title",
        "Test Type",
        "Priority",
        "Current Classification",
        "Cycle ID",
        "Cycle Name",
        "Cycle Status",
        "Release",
        "Environment",
        "Execution Mode",
        "Result",
        "Automation ID",
        "Automation Version",
        "Automation Engine",
        "Automation Language",
        "Execution ID",
        "Execution Status",
        "Exit Code",
        "Duration (ms)",
        "Screenshot Available",
        "Trace Available",
        "Actual Result",
        "Comment",
        "Defect Reference",
    ]


    worksheet.append(
        headers
    )


    header_row = 3


    style_header_row(
        worksheet,
        header_row
    )


    for requirement in (
        traceability.requirements
    ):

        for scenario in (
            requirement.scenarios
        ):

            for test_case in (
                scenario.test_cases
            ):

                occurrences = (
                    test_case.occurrences
                    or
                    []
                )


                if not occurrences:

                    worksheet.append(
                        [
                            requirement
                            .requirement_id,

                            requirement.title,

                            scenario.scenario_id,

                            scenario.title,

                            test_case.test_case_id,

                            test_case.title,

                            test_case.test_type,

                            test_case.priority,

                            test_case
                            .current_execution_type,

                            None,
                            None,
                            None,
                            None,
                            None,
                            None,
                            "NOT COVERED",
                            None,
                            None,
                            None,
                            None,
                            None,
                            None,
                            None,
                            None,
                            False,
                            False,
                            None,
                            None,
                            None,
                        ]
                    )


                    continue


                for occurrence in (
                    occurrences
                ):

                    execution = (
                        occurrence.execution
                    )


                    worksheet.append(
                        [
                            requirement
                            .requirement_id,

                            requirement.title,

                            scenario.scenario_id,

                            scenario.title,

                            test_case.test_case_id,

                            test_case.title,

                            test_case.test_type,

                            test_case.priority,

                            test_case
                            .current_execution_type,

                            occurrence.cycle_id,

                            occurrence.cycle_name,

                            display_status(
                                occurrence
                                .cycle_status
                            ),

                            occurrence.release,

                            occurrence.environment,

                            display_status(
                                occurrence
                                .execution_mode
                            ),

                            display_status(
                                occurrence
                                .result_status
                            ),

                            occurrence
                            .automation_version_id,

                            occurrence
                            .automation_version_number,

                            occurrence
                            .automation_engine,

                            occurrence
                            .automation_language,

                            (
                                execution.id
                                if execution
                                else None
                            ),

                            (
                                display_status(
                                    execution.status
                                )
                                if execution
                                else None
                            ),

                            (
                                execution.exit_code
                                if execution
                                else None
                            ),

                            (
                                execution.duration_ms
                                if execution
                                else None
                            ),

                            (
                                execution
                                .screenshot_available
                                if execution
                                else False
                            ),

                            (
                                execution
                                .trace_available
                                if execution
                                else False
                            ),

                            occurrence.actual_result,

                            occurrence.comment,

                            occurrence
                            .defect_reference,
                        ]
                    )


    style_data_area(
        worksheet,
        header_row + 1,
        worksheet.max_row,
        1,
        len(
            headers
        )
    )


    worksheet.freeze_panes = "A4"

    worksheet.auto_filter.ref = (
        f"A3:AC{worksheet.max_row}"
    )


    for column_number in range(
        1,
        len(
            headers
        ) + 1
    ):

        worksheet.column_dimensions[
            get_column_letter(
                column_number
            )
        ].width = 18


    for column in {
        "B",
        "D",
        "F",
        "K",
        "AA",
        "AB",
        "AC",
    }:

        worksheet.column_dimensions[
            column
        ].width = 36


def build_release_quality_excel(
    *,
    project_name: str,
    release_quality,
    traceability
) -> bytes:

    workbook = Workbook()


    add_summary_sheet(
        workbook,
        project_name,
        release_quality
    )


    add_reasons_sheet(
        workbook,
        release_quality
    )


    add_risks_sheet(
        workbook,
        release_quality
    )


    add_traceability_sheet(
        workbook,
        traceability
    )


    output = BytesIO()


    workbook.save(
        output
    )


    content = output.getvalue()


    output.close()


    return content
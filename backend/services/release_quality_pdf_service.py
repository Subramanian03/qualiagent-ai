from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak
from reportlab.platypus import Paragraph
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Spacer
from reportlab.platypus import Table
from reportlab.platypus import TableStyle


SIGNAL_COLORS = {
    "ready": colors.HexColor(
        "#166534"
    ),

    "at_risk": colors.HexColor(
        "#92400E"
    ),

    "not_ready": colors.HexColor(
        "#991B1B"
    ),
}


SIGNAL_BACKGROUNDS = {
    "ready": colors.HexColor(
        "#DCFCE7"
    ),

    "at_risk": colors.HexColor(
        "#FEF3C7"
    ),

    "not_ready": colors.HexColor(
        "#FEE2E2"
    ),
}


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


def safe_paragraph_text(
    value,
    default: str = ""
) -> str:

    return escape(
        clean_text(
            value,
            default
        )
    )


def display_status(
    value,
    default: str = "UNKNOWN"
) -> str:

    cleaned = clean_text(
        value,
        default
    )


    return (
        cleaned
        .replace(
            "_",
            " "
        )
        .upper()
    )


def format_environment(
    value
) -> str:

    return clean_text(
        value,
        "All Environments"
    )

def safe_filename_part(
    value,
    default: str
) -> str:

    source = clean_text(
        value,
        default
    )


    cleaned = "".join(
        character
        if (
            character.isalnum()
            or
            character in {
                "-",
                "_",
            }
        )
        else "-"
        for character in source
    )


    cleaned = cleaned.strip(
        "-"
    )


    return (
        cleaned
        if cleaned
        else default
    )

def build_styles():

    styles = getSampleStyleSheet()


    styles.add(
        ParagraphStyle(
            name="ReportTitle",
            parent=styles[
                "Title"
            ],
            fontName="Helvetica-Bold",
            fontSize=20,
            leading=24,
            textColor=colors.HexColor(
                "#101828"
            ),
            alignment=TA_LEFT,
            spaceAfter=8
        )
    )


    styles.add(
        ParagraphStyle(
            name="ReportSubtitle",
            parent=styles[
                "Normal"
            ],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=colors.HexColor(
                "#475467"
            ),
            spaceAfter=12
        )
    )


    styles.add(
        ParagraphStyle(
            name="SectionHeading",
            parent=styles[
                "Heading2"
            ],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=16,
            textColor=colors.HexColor(
                "#101828"
            ),
            spaceBefore=10,
            spaceAfter=8
        )
    )


    styles.add(
        ParagraphStyle(
            name="SmallLabel",
            parent=styles[
                "Normal"
            ],
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=10,
            textColor=colors.HexColor(
                "#667085"
            ),
            spaceAfter=3
        )
    )


    styles.add(
        ParagraphStyle(
            name="BodySmall",
            parent=styles[
                "Normal"
            ],
            fontName="Helvetica",
            fontSize=8,
            leading=11,
            textColor=colors.HexColor(
                "#344054"
            )
        )
    )


    styles.add(
        ParagraphStyle(
            name="BodySmallBold",
            parent=styles[
                "BodySmall"
            ],
            fontName="Helvetica-Bold"
        )
    )


    styles.add(
        ParagraphStyle(
            name="Signal",
            parent=styles[
                "Normal"
            ],
            fontName="Helvetica-Bold",
            fontSize=15,
            leading=18,
            alignment=TA_CENTER
        )
    )


    return styles


def build_metric_table(
    release_quality,
    styles
):

    execution = (
        release_quality.execution
    )


    rows = [
        [
            "Test Cycles",
            execution.cycles,
            "Completed Cycles",
            execution.completed_cycles,
        ],
        [
            "Planned Tests",
            execution.planned_tests,
            "Completed Tests",
            execution.completed_tests,
        ],
        [
            "Passed",
            execution.passed,
            "Failed",
            execution.failed,
        ],
        [
            "Blocked",
            execution.blocked,
            "Not Run",
            execution.not_run,
        ],
        [
            "Running",
            execution.running,
            "Errors",
            execution.error,
        ],
        [
            "Skipped",
            execution.skipped,
            "Pass Rate",
            f"{execution.pass_rate}%",
        ],
    ]


    table_data = []


    for row in rows:

        table_data.append(
            [
                Paragraph(
                    safe_paragraph_text(
                        row[0]
                    ),
                    styles[
                        "BodySmall"
                    ]
                ),

                Paragraph(
                    safe_paragraph_text(
                        row[1]
                    ),
                    styles[
                        "BodySmallBold"
                    ]
                ),

                Paragraph(
                    safe_paragraph_text(
                        row[2]
                    ),
                    styles[
                        "BodySmall"
                    ]
                ),

                Paragraph(
                    safe_paragraph_text(
                        row[3]
                    ),
                    styles[
                        "BodySmallBold"
                    ]
                ),
            ]
        )


    table = Table(
        table_data,
        colWidths=[
            42 * mm,
            22 * mm,
            42 * mm,
            22 * mm,
        ],
        hAlign="LEFT"
    )


    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (
                        0,
                        0
                    ),
                    (
                        -1,
                        -1
                    ),
                    colors.HexColor(
                        "#F8FAFC"
                    )
                ),
                (
                    "GRID",
                    (
                        0,
                        0
                    ),
                    (
                        -1,
                        -1
                    ),
                    0.5,
                    colors.HexColor(
                        "#D0D5DD"
                    )
                ),
                (
                    "VALIGN",
                    (
                        0,
                        0
                    ),
                    (
                        -1,
                        -1
                    ),
                    "MIDDLE"
                ),
                (
                    "LEFTPADDING",
                    (
                        0,
                        0
                    ),
                    (
                        -1,
                        -1
                    ),
                    7
                ),
                (
                    "RIGHTPADDING",
                    (
                        0,
                        0
                    ),
                    (
                        -1,
                        -1
                    ),
                    7
                ),
                (
                    "TOPPADDING",
                    (
                        0,
                        0
                    ),
                    (
                        -1,
                        -1
                    ),
                    7
                ),
                (
                    "BOTTOMPADDING",
                    (
                        0,
                        0
                    ),
                    (
                        -1,
                        -1
                    ),
                    7
                ),
            ]
        )
    )


    return table


def build_execution_mode_table(
    release_quality,
    styles
):

    modes = (
        release_quality.execution_modes
    )


    table_data = [
        [
            Paragraph(
                "Mode",
                styles[
                    "BodySmallBold"
                ]
            ),
            Paragraph(
                "Total",
                styles[
                    "BodySmallBold"
                ]
            ),
            Paragraph(
                "Passed",
                styles[
                    "BodySmallBold"
                ]
            ),
            Paragraph(
                "Failed",
                styles[
                    "BodySmallBold"
                ]
            ),
            Paragraph(
                "Blocked",
                styles[
                    "BodySmallBold"
                ]
            ),
            Paragraph(
                "Skipped / Error",
                styles[
                    "BodySmallBold"
                ]
            ),
        ],
        [
            Paragraph(
                "Manual",
                styles[
                    "BodySmall"
                ]
            ),
            modes.manual_total,
            modes.manual_passed,
            modes.manual_failed,
            modes.manual_blocked,
            modes.manual_skipped,
        ],
        [
            Paragraph(
                "Automation",
                styles[
                    "BodySmall"
                ]
            ),
            modes.automation_total,
            modes.automation_passed,
            modes.automation_failed,
            "-",
            modes.automation_error,
        ],
    ]


    table = Table(
        table_data,
        colWidths=[
            33 * mm,
            21 * mm,
            21 * mm,
            21 * mm,
            24 * mm,
            30 * mm,
        ],
        repeatRows=1,
        hAlign="LEFT"
    )


    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (
                        0,
                        0
                    ),
                    (
                        -1,
                        0
                    ),
                    colors.HexColor(
                        "#EAF0F7"
                    )
                ),
                (
                    "GRID",
                    (
                        0,
                        0
                    ),
                    (
                        -1,
                        -1
                    ),
                    0.5,
                    colors.HexColor(
                        "#D0D5DD"
                    )
                ),
                (
                    "VALIGN",
                    (
                        0,
                        0
                    ),
                    (
                        -1,
                        -1
                    ),
                    "MIDDLE"
                ),
                (
                    "ALIGN",
                    (
                        1,
                        1
                    ),
                    (
                        -1,
                        -1
                    ),
                    "CENTER"
                ),
                (
                    "LEFTPADDING",
                    (
                        0,
                        0
                    ),
                    (
                        -1,
                        -1
                    ),
                    6
                ),
                (
                    "RIGHTPADDING",
                    (
                        0,
                        0
                    ),
                    (
                        -1,
                        -1
                    ),
                    6
                ),
                (
                    "TOPPADDING",
                    (
                        0,
                        0
                    ),
                    (
                        -1,
                        -1
                    ),
                    7
                ),
                (
                    "BOTTOMPADDING",
                    (
                        0,
                        0
                    ),
                    (
                        -1,
                        -1
                    ),
                    7
                ),
            ]
        )
    )


    return table


def build_reason_elements(
    release_quality,
    styles
):

    elements = []


    reasons = (
        release_quality.reasons
        or
        []
    )


    if not reasons:

        elements.append(
            Paragraph(
                "No readiness reasons were returned.",
                styles[
                    "BodySmall"
                ]
            )
        )


        return elements


    for reason in reasons:

        code = display_status(
            reason.code,
            "REASON"
        )


        message = safe_paragraph_text(
            reason.message
        )


        elements.append(
            Table(
                [
                    [
                        Paragraph(
                            safe_paragraph_text(
                                code
                            ),
                            styles[
                                "BodySmallBold"
                            ]
                        ),

                        Paragraph(
                            message,
                            styles[
                                "BodySmall"
                            ]
                        ),
                    ]
                ],
                colWidths=[
                    35 * mm,
                    115 * mm,
                ],
                style=TableStyle(
                    [
                        (
                            "BACKGROUND",
                            (
                                0,
                                0
                            ),
                            (
                                -1,
                                -1
                            ),
                            colors.HexColor(
                                "#F8FAFC"
                            )
                        ),
                        (
                            "BOX",
                            (
                                0,
                                0
                            ),
                            (
                                -1,
                                -1
                            ),
                            0.5,
                            colors.HexColor(
                                "#D0D5DD"
                            )
                        ),
                        (
                            "VALIGN",
                            (
                                0,
                                0
                            ),
                            (
                                -1,
                                -1
                            ),
                            "TOP"
                        ),
                        (
                            "LEFTPADDING",
                            (
                                0,
                                0
                            ),
                            (
                                -1,
                                -1
                            ),
                            7
                        ),
                        (
                            "RIGHTPADDING",
                            (
                                0,
                                0
                            ),
                            (
                                -1,
                                -1
                            ),
                            7
                        ),
                        (
                            "TOPPADDING",
                            (
                                0,
                                0
                            ),
                            (
                                -1,
                                -1
                            ),
                            7
                        ),
                        (
                            "BOTTOMPADDING",
                            (
                                0,
                                0
                            ),
                            (
                                -1,
                                -1
                            ),
                            7
                        ),
                    ]
                )
            )
        )


        elements.append(
            Spacer(
                1,
                5
            )
        )


    return elements


def build_risk_elements(
    release_quality,
    styles
):

    elements = []


    risks = (
        release_quality.risks
        or
        []
    )


    if not risks:

        elements.append(
            Paragraph(
                (
                    "No direct Test Case risks were "
                    "identified for this Release "
                    "and Environment."
                ),
                styles[
                    "BodySmall"
                ]
            )
        )


        return elements


    for index, risk in enumerate(
        risks,
        start=1
    ):

        execution = (
            risk.execution
        )


        evidence = []


        if (
            execution is not None
            and
            execution.screenshot_available
        ):

            evidence.append(
                "Screenshot"
            )


        if (
            execution is not None
            and
            execution.trace_available
        ):

            evidence.append(
                "Trace"
            )


        evidence_text = (
            ", ".join(
                evidence
            )
            if evidence
            else "None"
        )


        automation_text = "N/A"


        if risk.automation_version_id is not None:

            engine = display_status(
                risk.automation_engine,
                "AUTOMATION"
            )


            version = (
                f" V{risk.automation_version_number}"
                if (
                    risk.automation_version_number
                    is not None
                )
                else ""
            )


            automation_text = (
                f"{engine}{version} "
                f"(ID {risk.automation_version_id})"
            )


        execution_text = (
            f"Execution #{execution.id}"
            if execution is not None
            else "No Execution record"
        )


        title = (
            f"{index}. "
            f"{display_status(risk.severity)} - "
            f"{display_status(risk.result_status)}"
        )


        details = [
            [
                "Test Case",
                risk.test_case_id,
            ],
            [
                "Title",
                risk.test_case_title,
            ],
            [
                "Requirement",
                (
                    f"{risk.requirement_id} - "
                    f"{risk.requirement_title}"
                ),
            ],
            [
                "Scenario",
                (
                    f"{risk.scenario_id} - "
                    f"{risk.scenario_title}"
                ),
            ],
            [
                "Cycle",
                (
                    f"{risk.cycle_name} "
                    f"(#{risk.cycle_id})"
                ),
            ],
            [
                "Execution Mode",
                display_status(
                    risk.execution_mode
                ),
            ],
            [
                "Frozen Automation",
                automation_text,
            ],
            [
                "Execution",
                execution_text,
            ],
            [
                "Evidence",
                evidence_text,
            ],
        ]


        detail_rows = []


        for label, value in details:

            detail_rows.append(
                [
                    Paragraph(
                        safe_paragraph_text(
                            label
                        ),
                        styles[
                            "BodySmallBold"
                        ]
                    ),

                    Paragraph(
                        safe_paragraph_text(
                            value,
                            "N/A"
                        ),
                        styles[
                            "BodySmall"
                        ]
                    ),
                ]
            )


        risk_table = Table(
            [
                [
                    Paragraph(
                        safe_paragraph_text(
                            title
                        ),
                        styles[
                            "BodySmallBold"
                        ]
                    )
                ],
                [
                    Table(
                        detail_rows,
                        colWidths=[
                            36 * mm,
                            112 * mm,
                        ]
                    )
                ],
            ],
            colWidths=[
                154 * mm
            ],
            hAlign="LEFT"
        )


        risk_color = (
            colors.HexColor(
                "#FEE2E2"
            )
            if risk.severity == "blocker"
            else colors.HexColor(
                "#FEF3C7"
            )
        )


        risk_table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (
                            0,
                            0
                        ),
                        (
                            0,
                            0
                        ),
                        risk_color
                    ),
                    (
                        "BOX",
                        (
                            0,
                            0
                        ),
                        (
                            -1,
                            -1
                        ),
                        0.7,
                        colors.HexColor(
                            "#D0D5DD"
                        )
                    ),
                    (
                        "VALIGN",
                        (
                            0,
                            0
                        ),
                        (
                            -1,
                            -1
                        ),
                        "TOP"
                    ),
                    (
                        "LEFTPADDING",
                        (
                            0,
                            0
                        ),
                        (
                            -1,
                            -1
                        ),
                        7
                    ),
                    (
                        "RIGHTPADDING",
                        (
                            0,
                            0
                        ),
                        (
                            -1,
                            -1
                        ),
                        7
                    ),
                    (
                        "TOPPADDING",
                        (
                            0,
                            0
                        ),
                        (
                            -1,
                            -1
                        ),
                        7
                    ),
                    (
                        "BOTTOMPADDING",
                        (
                            0,
                            0
                        ),
                        (
                            -1,
                            -1
                        ),
                        7
                    ),
                ]
            )
        )


        elements.append(
            risk_table
        )


        elements.append(
            Spacer(
                1,
                8
            )
        )


    return elements


def add_page_number(
    canvas,
    document
):

    canvas.saveState()


    page_number = (
        canvas.getPageNumber()
    )


    canvas.setFont(
        "Helvetica",
        8
    )


    canvas.setFillColor(
        colors.HexColor(
            "#667085"
        )
    )


    canvas.drawRightString(
        A4[0] -
        document.rightMargin,
        12 * mm,
        f"Page {page_number}"
    )


    canvas.restoreState()


def build_release_quality_pdf(
    *,
    project_name: str,
    release_quality
) -> bytes:

    output = BytesIO()


    document = SimpleDocTemplate(
        output,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=20 * mm,
        title=(
            "QualiAgent Release Quality Report"
        ),
        author="QualiAgent AI"
    )


    styles = build_styles()


    signal = clean_text(
        release_quality.signal,
        "unknown"
    ).lower()


    signal_color = (
        SIGNAL_COLORS.get(
            signal,
            colors.HexColor(
                "#475467"
            )
        )
    )


    signal_background = (
        SIGNAL_BACKGROUNDS.get(
            signal,
            colors.HexColor(
                "#EEF2F6"
            )
        )
    )


    story = [
        Paragraph(
            "QualiAgent Release Quality Report",
            styles[
                "ReportTitle"
            ]
        ),

        Paragraph(
            (
                f"Project: "
                f"{safe_paragraph_text(project_name)}"
                f"<br/>Release: "
                f"{safe_paragraph_text(release_quality.release)}"
                f"<br/>Environment: "
                f"{safe_paragraph_text(format_environment(release_quality.environment))}"
            ),
            styles[
                "ReportSubtitle"
            ]
        ),

        Table(
            [
                [
                    Paragraph(
                        (
                            "RELEASE SIGNAL"
                            f"<br/><font size='15'>"
                            f"{safe_paragraph_text(display_status(signal))}"
                            "</font>"
                        ),
                        styles[
                            "Signal"
                        ]
                    )
                ]
            ],
            colWidths=[
                154 * mm
            ],
            style=TableStyle(
                [
                    (
                        "BACKGROUND",
                        (
                            0,
                            0
                        ),
                        (
                            -1,
                            -1
                        ),
                        signal_background
                    ),
                    (
                        "TEXTCOLOR",
                        (
                            0,
                            0
                        ),
                        (
                            -1,
                            -1
                        ),
                        signal_color
                    ),
                    (
                        "BOX",
                        (
                            0,
                            0
                        ),
                        (
                            -1,
                            -1
                        ),
                        0.8,
                        signal_color
                    ),
                    (
                        "TOPPADDING",
                        (
                            0,
                            0
                        ),
                        (
                            -1,
                            -1
                        ),
                        11
                    ),
                    (
                        "BOTTOMPADDING",
                        (
                            0,
                            0
                        ),
                        (
                            -1,
                            -1
                        ),
                        11
                    ),
                ]
            )
        ),

        Spacer(
            1,
            10
        ),

        Paragraph(
            "Execution Summary",
            styles[
                "SectionHeading"
            ]
        ),

        build_metric_table(
            release_quality,
            styles
        ),

        Paragraph(
            "Manual vs Automation",
            styles[
                "SectionHeading"
            ]
        ),

        build_execution_mode_table(
            release_quality,
            styles
        ),

        Paragraph(
            "Evidence Summary",
            styles[
                "SectionHeading"
            ]
        ),

        Table(
            [
                [
                    "Executions",
                    release_quality
                    .evidence
                    .executions,

                    "Screenshots",
                    release_quality
                    .evidence
                    .screenshots,

                    "Traces",
                    release_quality
                    .evidence
                    .traces,
                ]
            ],
            colWidths=[
                28 * mm,
                18 * mm,
                28 * mm,
                18 * mm,
                22 * mm,
                18 * mm,
            ],
            style=TableStyle(
                [
                    (
                        "BACKGROUND",
                        (
                            0,
                            0
                        ),
                        (
                            -1,
                            -1
                        ),
                        colors.HexColor(
                            "#F8FAFC"
                        )
                    ),
                    (
                        "GRID",
                        (
                            0,
                            0
                        ),
                        (
                            -1,
                            -1
                        ),
                        0.5,
                        colors.HexColor(
                            "#D0D5DD"
                        )
                    ),
                    (
                        "FONTNAME",
                        (
                            0,
                            0
                        ),
                        (
                            -1,
                            -1
                        ),
                        "Helvetica"
                    ),
                    (
                        "ALIGN",
                        (
                            1,
                            0
                        ),
                        (
                            1,
                            0
                        ),
                        "CENTER"
                    ),
                    (
                        "ALIGN",
                        (
                            3,
                            0
                        ),
                        (
                            3,
                            0
                        ),
                        "CENTER"
                    ),
                    (
                        "ALIGN",
                        (
                            5,
                            0
                        ),
                        (
                            5,
                            0
                        ),
                        "CENTER"
                    ),
                    (
                        "TOPPADDING",
                        (
                            0,
                            0
                        ),
                        (
                            -1,
                            -1
                        ),
                        7
                    ),
                    (
                        "BOTTOMPADDING",
                        (
                            0,
                            0
                        ),
                        (
                            -1,
                            -1
                        ),
                        7
                    ),
                ]
            )
        ),

        Paragraph(
            "Readiness Reasons",
            styles[
                "SectionHeading"
            ]
        ),
    ]


    story.extend(
        build_reason_elements(
            release_quality,
            styles
        )
    )


    story.append(
        PageBreak()
    )


    story.append(
        Paragraph(
            "Release Risks",
            styles[
                "SectionHeading"
            ]
        )
    )


    story.extend(
        build_risk_elements(
            release_quality,
            styles
        )
    )


    story.append(
        Spacer(
            1,
            10
        )
    )


    story.append(
        Paragraph(
            (
                "This report is generated from "
                "the Test Cycle history stored "
                "by QualiAgent. The release signal "
                "is deterministic and is not an "
                "AI-generated approval decision."
            ),
            styles[
                "BodySmall"
            ]
        )
    )


    document.build(
        story,
        onFirstPage=add_page_number,
        onLaterPages=add_page_number
    )


    pdf_bytes = output.getvalue()


    output.close()


    return pdf_bytes
import os
import shutil
import subprocess

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parents[2]
)


RUNNER_ROOT = (
    PROJECT_ROOT /
    "runner"
).resolve()


GENERATED_TEST_ROOT = (
    RUNNER_ROOT /
    "tests" /
    "generated"
).resolve()


EVIDENCE_ROOT = (
    RUNNER_ROOT /
    "evidence"
).resolve()


PLAYWRIGHT_TIMEOUT_SECONDS = 180


@dataclass
class PlaywrightRunResult:

    exit_code: int | None

    stdout: str

    stderr: str

    infrastructure_error: str | None

    started_at: datetime

    completed_at: datetime

    duration_ms: int

    screenshot_path: str | None

    trace_path: str | None


def run_playwright(
    *,
    execution_id: int,
    automation_code: str,
    runtime_environment:
        dict[str, str]
) -> PlaywrightRunResult:

    started_at = datetime.utcnow()


    GENERATED_TEST_ROOT.mkdir(
        parents=True,
        exist_ok=True
    )


    execution_evidence_root = (
        EVIDENCE_ROOT /
        f"execution-{execution_id}"
    )


    execution_evidence_root.mkdir(
        parents=True,
        exist_ok=True
    )


    generated_test_path = (
        GENERATED_TEST_ROOT /
        f"execution-{execution_id}.spec.js"
    )


    screenshot_path = (
        execution_evidence_root /
        "failure.png"
    )


    trace_path = (
        execution_evidence_root /
        "trace.zip"
    )


    try:

        generated_test_path.write_text(
            automation_code,
            encoding="utf-8"
        )

    except OSError:

        completed_at = datetime.utcnow()

        return PlaywrightRunResult(
            exit_code=None,
            stdout="",
            stderr="",
            infrastructure_error=(
                "Unable to write the generated "
                "Playwright test file"
            ),
            started_at=started_at,
            completed_at=completed_at,
            duration_ms=calculate_duration_ms(
                started_at,
                completed_at
            ),
            screenshot_path=None,
            trace_path=None
        )


    process_environment = {
        **os.environ,

        **{
            key: str(value)
            for key, value
            in runtime_environment.items()
        },

        "QUALIAGENT_EXECUTION_ID":
            str(execution_id),

        "QUALIAGENT_SCREENSHOT_PATH":
            str(screenshot_path),

        "QUALIAGENT_TRACE_PATH":
            str(trace_path),

        "QUALIAGENT_EVIDENCE_DIR":
        str(execution_evidence_root),
    }


    # Resolve the Windows npx command.
    npx_command = (
        shutil.which(
            "npx.cmd"
        )
        or shutil.which(
            "npx"
        )
    )


    if not npx_command:

        completed_at = datetime.utcnow()

        return PlaywrightRunResult(
            exit_code=None,
            stdout="",
            stderr="",
            infrastructure_error=(
                "Node.js npx was not found "
                "in the backend process PATH"
            ),
            started_at=started_at,
            completed_at=completed_at,
            duration_ms=calculate_duration_ms(
                started_at,
                completed_at
            ),
            screenshot_path=None,
            trace_path=None
        )


    relative_test_path = (
    generated_test_path
    .relative_to(
        RUNNER_ROOT
    )
)


    command = [
    npx_command,
    "playwright",
    "test",
    relative_test_path.as_posix(),
    "--config",
    "playwright.execution.config.js",
]


    try:

        completed = subprocess.run(
            command,
            cwd=str(RUNNER_ROOT),
            env=process_environment,
            capture_output=True,
            text=True,
            timeout=(
                PLAYWRIGHT_TIMEOUT_SECONDS
            ),
            shell=False
        )


        completed_at = datetime.utcnow()


        detected_trace_path = (
            find_trace_file(
                execution_evidence_root,
                RUNNER_ROOT
            )
        )


        detected_screenshot_path = (
            find_screenshot_file(
                execution_evidence_root,
                RUNNER_ROOT
            )
        )


        return PlaywrightRunResult(
            exit_code=(
                completed.returncode
            ),
            stdout=(
                completed.stdout or ""
            ),
            stderr=(
                completed.stderr or ""
            ),
            infrastructure_error=None,
            started_at=started_at,
            completed_at=completed_at,
            duration_ms=calculate_duration_ms(
                started_at,
                completed_at
            ),
            screenshot_path=(
                str(detected_screenshot_path)
                if detected_screenshot_path
                else None
            ),
            trace_path=(
                str(detected_trace_path)
                if detected_trace_path
                else None
            )
        )


    except subprocess.TimeoutExpired as exc:

        completed_at = datetime.utcnow()


        return PlaywrightRunResult(
            exit_code=None,
            stdout=normalise_subprocess_output(
                exc.stdout
            ),
            stderr=normalise_subprocess_output(
                exc.stderr
            ),
            infrastructure_error=(
                "Playwright execution exceeded "
                f"{PLAYWRIGHT_TIMEOUT_SECONDS} "
                "seconds"
            ),
            started_at=started_at,
            completed_at=completed_at,
            duration_ms=calculate_duration_ms(
                started_at,
                completed_at
            ),
            screenshot_path=(
                str(screenshot_path)
                if screenshot_path.is_file()
                else None
            ),
            trace_path=(
                str(trace_path)
                if trace_path.is_file()
                else None
            )
        )


    except FileNotFoundError:

        completed_at = datetime.utcnow()


        return PlaywrightRunResult(
            exit_code=None,
            stdout="",
            stderr="",
            infrastructure_error=(
                "The Node.js npx command was "
                "not found. Confirm Node.js and "
                "the Playwright runner "
                "dependencies are installed."
            ),
            started_at=started_at,
            completed_at=completed_at,
            duration_ms=calculate_duration_ms(
                started_at,
                completed_at
            ),
            screenshot_path=None,
            trace_path=None
        )


    except OSError:

        completed_at = datetime.utcnow()


        return PlaywrightRunResult(
            exit_code=None,
            stdout="",
            stderr="",
            infrastructure_error=(
                "The Playwright process could "
                "not be started"
            ),
            started_at=started_at,
            completed_at=completed_at,
            duration_ms=calculate_duration_ms(
                started_at,
                completed_at
            ),
            screenshot_path=None,
            trace_path=None
        )


def calculate_duration_ms(
    started_at: datetime,
    completed_at: datetime
) -> int:

    duration = (
        completed_at -
        started_at
    )

    return max(
        0,
        int(
            duration.total_seconds()
            * 1000
        )
    )


def normalise_subprocess_output(
    value
) -> str:

    if value is None:
        return ""


    if isinstance(
        value,
        bytes
    ):

        return value.decode(
            "utf-8",
            errors="replace"
        )


    return str(
        value
    )


def find_trace_file(
    execution_evidence_root: Path,
    runner_root: Path
) -> Path | None:

    candidates = list(
        execution_evidence_root.rglob(
            "trace.zip"
        )
    )

    valid_candidates = [
        path
        for path in candidates
        if path.is_file()
    ]

    if not valid_candidates:
        return None

    return max(
        valid_candidates,
        key=lambda path:
            path.stat().st_mtime
    )
def find_screenshot_file(
    execution_evidence_root: Path,
    runner_root: Path
) -> Path | None:

    candidates = list(
        execution_evidence_root.rglob(
            "*.png"
        )
    )

    valid_candidates = [
        path
        for path in candidates
        if path.is_file()
    ]

    if not valid_candidates:
        return None

    return max(
        valid_candidates,
        key=lambda path:
            path.stat().st_mtime
    )
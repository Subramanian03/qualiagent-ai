from pathlib import Path

from fastapi.responses import FileResponse
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.db.database import get_db
from backend.models.execution import (
    ExecutionCreate,
    ExecutionResponse,
    ProjectExecutionResponse,
)
from backend.services.execution_service import (
    create_execution,
    get_automation_executions,
    get_automation_script,
    get_execution,
    build_project_execution_response,
    get_project_executions,
)
from backend.services.execution_runner_service import (
    run_execution,
)

from backend.db.project_model import (
    ProjectDB,
)

from backend.ai.errors import (
    AIProviderError,
    AIProviderConfigurationError,
    AIProviderResponseError,
    AIProviderUnavailableError,
)

from backend.models.execution_runtime import (
    ExecutionRuntimeRequest,
)

from backend.services.execution_runtime_service import (
    build_execution_environment,
    prepare_execution_runtime,
)

from backend.db.automation_model import (
    AutomationScriptDB,
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
from backend.automation_engines import (
    get_automation_engine,
)

from backend.automation_engines.errors import (
    AutomationEngineError,
)

from backend.models.failure_analysis import (
    FailureAnalysisResponse,
)

from backend.services.failure_analysis_service import (
    analyze_execution_failure,
)

PROJECT_ROOT = (
    Path(__file__).resolve().parents[2]
)

EVIDENCE_ROOT = (
    PROJECT_ROOT /
    "runner" /
    "evidence"
).resolve()

router = APIRouter(
    prefix="/api/executions",
    tags=["Executions"]
)

def resolve_execution_context(
    db: Session,
    execution
):

    automation = (
        db.query(AutomationScriptDB)
        .filter(
            AutomationScriptDB.id ==
            execution.automation_script_id
        )
        .first()
    )

    if automation is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Automation for Execution "
                "was not found"
            )
        )


    test_case = (
        db.query(TestCaseDB)
        .filter(
            TestCaseDB.id ==
            automation.test_case_db_id
        )
        .first()
    )

    if test_case is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Parent Test Case "
                "was not found"
            )
        )


    if test_case.test_scenario_db_id is None:
        raise HTTPException(
            status_code=409,
            detail=(
                "Test Case is not linked "
                "to a Test Scenario"
            )
        )


    scenario = (
        db.query(TestScenarioDB)
        .filter(
            TestScenarioDB.id ==
            test_case.test_scenario_db_id
        )
        .first()
    )

    if scenario is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Parent Test Scenario "
                "was not found"
            )
        )


    requirement = (
        db.query(RequirementDB)
        .filter(
            RequirementDB.id ==
            test_case.requirement_db_id
        )
        .first()
    )

    if requirement is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Parent Requirement "
                "was not found"
            )
        )


    if (
        scenario.requirement_db_id !=
        requirement.id
    ):
        raise HTTPException(
            status_code=409,
            detail=(
                "Scenario and Requirement "
                "traceability is inconsistent"
            )
        )


    project = (
        db.query(ProjectDB)
        .filter(
            ProjectDB.id ==
            requirement.project_id
        )
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Parent Project "
                "was not found"
            )
        )


    return (
        automation,
        test_case,
        scenario,
        requirement,
        project
    )

def get_safe_evidence_file(
    stored_path: str | None
) -> Path | None:

    if not stored_path:
        return None

    file_path = Path(
        stored_path
    ).resolve()

    try:
        file_path.relative_to(
            EVIDENCE_ROOT
        )
    except ValueError:
        return None

    if not file_path.is_file():
        return None

    return file_path

@router.post(
    "",
    response_model=ExecutionResponse,
    status_code=201
)
def create_execution_endpoint(
    request: ExecutionCreate,
    db: Session = Depends(get_db)
):

    automation = get_automation_script(
        db,
        request.automation_script_id
    )

    if automation is None:
        raise HTTPException(
            status_code=404,
            detail="Automation script not found"
        )

    if automation.status != "ready":
        raise HTTPException(
            status_code=409,
            detail=(
                "Only READY automation "
                "can create an execution"
            )
        )

    if not automation.code.strip():
        raise HTTPException(
            status_code=409,
            detail=(
                "Automation has no generated code"
            )
        )

    return create_execution(
        db,
        automation.id
    )


@router.get(
    "/{execution_id}",
    response_model=ExecutionResponse
)
def get_execution_endpoint(
    execution_id: int,
    db: Session = Depends(get_db)
):

    execution = get_execution(
        db,
        execution_id
    )

    if execution is None:
        raise HTTPException(
            status_code=404,
            detail="Execution not found"
        )

    return execution


@router.get(
    "/automation/{automation_script_id}",
    response_model=list[ExecutionResponse]
)
def list_automation_executions(
    automation_script_id: int,
    db: Session = Depends(get_db)
):

    automation = get_automation_script(
        db,
        automation_script_id
    )

    if automation is None:
        raise HTTPException(
            status_code=404,
            detail="Automation script not found"
        )

    return get_automation_executions(
        db,
        automation_script_id
    )

@router.post(
    "/{execution_id}/run",
    response_model=ExecutionResponse
)


def run_execution_endpoint(
    execution_id: int,
    request: ExecutionRuntimeRequest,
    db: Session = Depends(get_db)
):

    execution = get_execution(
        db,
        execution_id
    )


    if execution is None:

        raise HTTPException(
            status_code=404,
            detail="Execution not found"
        )


    (
        automation,
        test_case,
        scenario,
        requirement,
        project
    ) = resolve_execution_context(
        db,
        execution
    )


    if execution.status != "pending":

        raise HTTPException(
            status_code=409,
            detail=(
                "Only PENDING executions "
                "can be run"
            )
        )


    if automation.status != "ready":

        raise HTTPException(
            status_code=409,
            detail=(
                "Automation script "
                "is not READY"
            )
        )


    if not (
        automation.code and
        automation.code.strip()
    ):

        raise HTTPException(
            status_code=409,
            detail=(
                "Automation has no "
                "generated code"
            )
        )


    try:

        engine = (
            get_automation_engine(
                project
            )
        )


        (
            _input_schema,
            validated_inputs
        ) = prepare_execution_runtime(
            project=project,
            requirement=requirement,
            scenario=scenario,
            test_case=test_case,
            automation=automation,
            request=request
        )


        runtime_environment = (
            build_execution_environment(
                validated_inputs
            )
        )


    except AutomationEngineError as exc:

        raise HTTPException(
            status_code=409,
            detail=str(exc)
        ) from exc


    except AIProviderError as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc)
        ) from exc


    except ValueError as exc:

        raise HTTPException(
            status_code=422,
            detail=str(exc)
        ) from exc

        raise HTTPException(
            status_code=502,
            detail=str(exc)
        ) from exc


    except ValueError as exc:

        raise HTTPException(
            status_code=422,
            detail=str(exc)
        ) from exc


    try:

        return run_execution(
            db=db,
            execution=execution,
            automation=automation,
            engine=engine,
            runtime_environment=(
                runtime_environment
            )
        )


    except AutomationEngineError as exc:

        raise HTTPException(
            status_code=409,
            detail=str(exc)
        ) from exc

@router.get(
    "/{execution_id}/evidence/screenshot",
    response_class=FileResponse
)
def get_execution_screenshot(
    execution_id: int,
    db: Session = Depends(get_db)
):

    execution = get_execution(
        db,
        execution_id
    )

    if execution is None:
        raise HTTPException(
            status_code=404,
            detail="Execution not found"
        )

    screenshot = get_safe_evidence_file(
        execution.screenshot_path
    )

    if screenshot is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Screenshot evidence "
                "not available"
            )
        )

    return FileResponse(
        path=str(screenshot),
        media_type="image/png",
        filename=(
            f"execution-{execution.id}"
            "-screenshot.png"
        )
    )

@router.get(
    "/{execution_id}/evidence/trace",
    response_class=FileResponse
)
def get_execution_trace(
    execution_id: int,
    db: Session = Depends(get_db)
):

    execution = get_execution(
        db,
        execution_id
    )

    if execution is None:
        raise HTTPException(
            status_code=404,
            detail="Execution not found"
        )

    trace = get_safe_evidence_file(
        execution.trace_path
    )

    if trace is None:
        raise HTTPException(
            status_code=404,
            detail=(
    "Execution trace "
    "not available"
)
        )

    return FileResponse(
        path=str(trace),
        media_type="application/zip",
        filename=(
            f"execution-{execution.id}"
            "-trace.zip"
        )
    )
@router.get(
    "/project/{project_id}",
    response_model=list[
        ProjectExecutionResponse
    ]
)
def list_project_executions(
    project_id: int,
    db: Session = Depends(get_db)
):

    project = (
        db.query(ProjectDB)
        .filter(
            ProjectDB.id ==
            project_id
        )
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    rows = get_project_executions(
        db,
        project_id
    )

    return [
        build_project_execution_response(
            row
        )
        for row in rows
    ]

@router.post(
    "/{execution_id}/failure-analysis",
    response_model=FailureAnalysisResponse
)
def analyze_execution_failure_endpoint(
    execution_id: int,
    db: Session = Depends(get_db)
):

    try:

        return (
            analyze_execution_failure(
                db,
                execution_id
            )
        )


    except AIProviderConfigurationError as exc:

        raise HTTPException(
            status_code=503,
            detail=(
                "AI failure analysis is not "
                "configured correctly."
            )
        ) from exc


    except AIProviderUnavailableError as exc:

        raise HTTPException(
            status_code=503,
            detail=(
                "AI failure analysis provider "
                "is currently unavailable."
            )
        ) from exc


    except AIProviderResponseError as exc:

        raise HTTPException(
            status_code=502,
            detail=(
                "AI failure analysis returned "
                "an invalid provider response."
            )
        ) from exc


    except ValueError as exc:

        message = str(
            exc
        )


        if message == "Execution not found":

            raise HTTPException(
                status_code=404,
                detail=message
            ) from exc


        raise HTTPException(
            status_code=422,
            detail=message
        ) from exc
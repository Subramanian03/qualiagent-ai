from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from backend.db.database import (
    get_db,
)

from backend.db.project_model import (
    ProjectDB,
)

from backend.models.test_cycle import (
    CycleTestItemResponse,
    TestCycleCreate,
    TestCycleListItem,
    TestCycleResponse,
    TestCycleResultSummary,
    TestCycleStatusUpdate,
)

from backend.services.test_cycle_service import (
    TestCycleValidationError,
    create_test_cycle,
    get_project_test_cycles,
    get_test_cycle,
)

from backend.services.cycle_lifecycle_service import (
    TestCycleLifecycleError,
    get_cycle_for_lifecycle,
    get_cycle_result_summary,
    transition_test_cycle,
)

from backend.services.cycle_manual_result_service import (
    ManualCycleResultError,
    get_cycle_test_item,
    update_manual_cycle_result,
)

from backend.models.automation_input_schema import (
    AutomationInputSchema,
)

from backend.services.cycle_automation_runtime_service import (
    CycleAutomationRuntimeError,
    prepare_automated_cycle_item_inputs,
)
from backend.automation_engines.errors import (
    AutomationEngineError,
)
from backend.models.cycle_execution import (
    AutomatedCycleRunRequest,
    ManualCycleResultUpdate,
)
from backend.services.cycle_automation_execution_service import (
    CycleAutomationExecutionError,
    execute_automated_cycle_item,
)
from backend.services.project_isolation_service import (
    ProjectIsolationError,
    require_test_cycle_in_project,
    require_cycle_test_item_in_project,
)

router = APIRouter(
    tags=[
        "Test Cycles"
    ]
)


def get_project_or_404(
    db: Session,
    project_id: int
):

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

        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )


    return project


@router.post(
    "/api/projects/{project_id}/test-cycles",
    response_model=TestCycleResponse,
    status_code=201
)
def create_test_cycle_endpoint(
    project_id: int,
    request: TestCycleCreate,
    db: Session = Depends(get_db)
):

    project = get_project_or_404(
        db,
        project_id
    )


    try:

        return create_test_cycle(
            db,
            project=project,
            request=request
        )


    except TestCycleValidationError as exc:

        raise HTTPException(
            status_code=409,
            detail=str(exc)
        ) from exc


@router.get(
    "/api/projects/{project_id}/test-cycles",
    response_model=list[
        TestCycleListItem
    ]
)
def list_project_test_cycles_endpoint(
    project_id: int,
    db: Session = Depends(get_db)
):

    get_project_or_404(
        db,
        project_id
    )


    return get_project_test_cycles(
        db,
        project_id
    )


@router.get(
    "/api/projects/{project_id}/test-cycles/{cycle_id}",
    response_model=TestCycleResponse
)
def get_test_cycle_endpoint(
    project_id: int,
    cycle_id: int,
    db: Session = Depends(get_db)
):

    try:
        require_test_cycle_in_project(
            db,
            project_id=project_id,
            cycle_id=cycle_id
        )

    except ProjectIsolationError as exc:
        raise HTTPException(
            status_code=404,
            detail="Test Cycle not found"
        ) from exc


    cycle = get_test_cycle(
        db,
        cycle_id
    )


    if cycle is None:

        raise HTTPException(
            status_code=404,
            detail="Test Cycle not found"
        )


    return cycle

@router.get(
    "/api/projects/{project_id}/test-cycles/{cycle_id}/summary",
    response_model=TestCycleResultSummary
)
def get_test_cycle_summary_endpoint(
    project_id: int,
    cycle_id: int,
    db: Session = Depends(get_db)
):

    try:
        require_test_cycle_in_project(
            db,
            project_id=project_id,
            cycle_id=cycle_id
        )

    except ProjectIsolationError as exc:
        raise HTTPException(
            status_code=404,
            detail="Test Cycle not found"
        ) from exc


    cycle = get_cycle_for_lifecycle(
        db,
        cycle_id
    )


    if cycle is None:

        raise HTTPException(
            status_code=404,
            detail="Test Cycle not found"
        )


    return get_cycle_result_summary(
        cycle
    )

@router.patch(
    "/api/projects/{project_id}/test-cycles/"
    "{cycle_id}/status",
    response_model=TestCycleResponse
)
def update_test_cycle_status_endpoint(
    project_id: int,
    cycle_id: int,
    request: TestCycleStatusUpdate,
    db: Session = Depends(get_db)
):

    try:
        require_test_cycle_in_project(
            db,
            project_id=project_id,
            cycle_id=cycle_id
        )

    except ProjectIsolationError as exc:
        raise HTTPException(
            status_code=404,
            detail="Test Cycle not found"
        ) from exc

    cycle = get_cycle_for_lifecycle(
        db,
        cycle_id
    )

    if cycle is None:
        raise HTTPException(
            status_code=404,
            detail="Test Cycle not found"
        )


    try:

        return transition_test_cycle(
            db,
            cycle=cycle,
            requested_status=(
                request.status
            )
        )


    except TestCycleLifecycleError as exc:

        raise HTTPException(
            status_code=409,
            detail=str(exc)
        ) from exc

@router.patch(
    (
        "/api/projects/{project_id}/"
        "cycle-test-items/"
        "{cycle_item_id}/manual-result"
    ),
    response_model=CycleTestItemResponse
)
def update_manual_cycle_result_endpoint(
    project_id: int,
    cycle_item_id: int,
    request: ManualCycleResultUpdate,
    db: Session = Depends(get_db)
):

    try:
        cycle_item = (
            require_cycle_test_item_in_project(
                db,
                project_id=project_id,
                cycle_item_id=cycle_item_id
            )
        )

    except ProjectIsolationError as exc:
        raise HTTPException(
            status_code=404,
            detail="Cycle Test Item not found"
        ) from exc


    try:

        return update_manual_cycle_result(
            db,
            cycle_item=cycle_item,
            request=request
        )


    except (
        ManualCycleResultError,
        TestCycleLifecycleError
    ) as exc:

        raise HTTPException(
            status_code=409,
            detail=str(exc)
        ) from exc

@router.get(
    (
        "/api/projects/{project_id}/"
        "cycle-test-items/"
        "{cycle_item_id}/automation-inputs"
    ),
    response_model=AutomationInputSchema
)
def get_automated_cycle_item_inputs_endpoint(
    project_id: int,
    cycle_item_id: int,
    db: Session = Depends(get_db)
):

    try:
        cycle_item = (
            require_cycle_test_item_in_project(
                db,
                project_id=project_id,
                cycle_item_id=cycle_item_id
            )
        )

    except ProjectIsolationError as exc:
        raise HTTPException(
            status_code=404,
            detail="Cycle Test Item not found"
        ) from exc


    try:

        return (
            prepare_automated_cycle_item_inputs(
                db,
                cycle_item=cycle_item
            )
        )


    except (
        CycleAutomationRuntimeError,
        TestCycleLifecycleError
    ) as exc:

        raise HTTPException(
            status_code=409,
            detail=str(exc)
        ) from exc

@router.post(
    (
        "/api/projects/{project_id}/"
        "cycle-test-items/"
        "{cycle_item_id}/run-automation"
    ),
    response_model=CycleTestItemResponse
)
def run_automated_cycle_item_endpoint(
    project_id: int,
    cycle_item_id: int,
    request: AutomatedCycleRunRequest,
    db: Session = Depends(get_db)
):

    try:
        cycle_item = (
            require_cycle_test_item_in_project(
                db,
                project_id=project_id,
                cycle_item_id=cycle_item_id
            )
        )

    except ProjectIsolationError as exc:
        raise HTTPException(
            status_code=404,
            detail="Cycle Test Item not found"
        ) from exc


    try:

        return (
            execute_automated_cycle_item(
                db,
                cycle_item=cycle_item,
                request=request
            )
        )


    except (
        CycleAutomationExecutionError,
        CycleAutomationRuntimeError,
        TestCycleLifecycleError,
        AutomationEngineError
    ) as exc:

        raise HTTPException(
            status_code=409,
            detail=str(exc)
        ) from exc
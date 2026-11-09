from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from backend.ai.errors import (
    AIProviderError,
)

from backend.db.database import get_db

from backend.models.test_case import (
    TestCaseGenerationRequest,
    TestCaseGenerationResponse,
    PersistedTestCaseResponse,
    TestCaseStatusUpdate,
    TestCaseExecutionTypeUpdate,
)

from backend.services.requirement_service import (
    get_requirement,
)

from backend.services.test_case_persistence_service import (
    delete_requirement_test_cases,
    get_requirement_test_cases,
    get_scenario_test_cases,
    save_test_cases,
    update_test_case_status,
)

from backend.services.test_case_service import (
    generate_test_cases,
    generate_test_cases_for_saved_requirement,
    get_test_scenario,
    update_test_case_execution_type,
)

from backend.services.test_case_generation_service import (
    generate_and_save_ai_test_cases,
)
from backend.db.test_case_model import (
    TestCaseDB,
)




router = APIRouter(
    prefix="/api/test-cases",
    tags=["Test Cases"],
)


@router.post(
    "/generate",
    response_model=TestCaseGenerationResponse,
)
def generate_test_cases_endpoint(
    request: TestCaseGenerationRequest,
):

    return generate_test_cases(
        request.requirement
    )


@router.post(
    "/requirement/{requirement_db_id}/generate",
    response_model=list[
        PersistedTestCaseResponse
    ],
    status_code=201,
)
def generate_and_save_test_cases(
    requirement_db_id: int,
    db: Session = Depends(get_db),
):

    requirement = get_requirement(
        db,
        requirement_db_id,
    )

    if requirement is None:
        raise HTTPException(
            status_code=404,
            detail="Requirement not found",
        )

    existing_test_cases = (
        get_requirement_test_cases(
            db,
            requirement_db_id,
        )
    )

    if existing_test_cases:
        raise HTTPException(
            status_code=409,
            detail=(
                "Test cases already exist for "
                "this requirement"
            ),
        )

    generated = (
        generate_test_cases_for_saved_requirement(
            db,
            requirement,
        )
    )

    return save_test_cases(
        db,
        requirement_db_id,
        generated.test_cases,
    )


@router.get(
    "/requirement/{requirement_db_id}",
    response_model=list[
        PersistedTestCaseResponse
    ],
)
def list_requirement_test_cases(
    requirement_db_id: int,
    db: Session = Depends(get_db),
):

    requirement = get_requirement(
        db,
        requirement_db_id,
    )

    if requirement is None:
        raise HTTPException(
            status_code=404,
            detail="Requirement not found",
        )

    return get_requirement_test_cases(
        db,
        requirement_db_id,
    )


# NEW: Scenario -> Test Cases
@router.get(
    "/scenario/{scenario_db_id}",
    response_model=list[
        PersistedTestCaseResponse
    ],
)
def list_scenario_test_cases(
    scenario_db_id: int,
    db: Session = Depends(get_db),
):

    scenario = get_test_scenario(
        db,
        scenario_db_id,
    )

    if scenario is None:

        raise HTTPException(
            status_code=404,
            detail="Test scenario not found",
        )


    return get_scenario_test_cases(
        db,
        scenario_db_id,
    )

@router.post(
    "/scenario/{scenario_db_id}/generate",
    response_model=list[
        PersistedTestCaseResponse
    ],
    status_code=201,
)
def generate_scenario_test_cases(
    scenario_db_id: int,
    db: Session = Depends(get_db),
):

    scenario = get_test_scenario(
        db,
        scenario_db_id,
    )

    if scenario is None:
        raise HTTPException(
            status_code=404,
            detail="Test scenario not found",
        )


    requirement = get_requirement(
        db,
        scenario.requirement_db_id,
    )

    if requirement is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Parent requirement "
                "not found"
            ),
        )


    existing_test_cases = (
        get_scenario_test_cases(
            db,
            scenario_db_id,
        )
    )


    if existing_test_cases:
        raise HTTPException(
            status_code=409,
            detail=(
                "Test Cases already exist "
                "for this Scenario"
            ),
        )


    try:

        return (
            generate_and_save_ai_test_cases(
                db=db,
                requirement=requirement,
                scenario=scenario,
            )
        )


    except AIProviderError as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc


    except ValueError as exc:

        db.rollback()

        raise HTTPException(
            status_code=409,
            detail=str(exc),
        ) from exc


    except IntegrityError as exc:

        db.rollback()

        raise HTTPException(
            status_code=409,
            detail=(
                "Test Case persistence "
                "conflict occurred"
            ),
        ) from exc

@router.post(
    "/requirement/{requirement_db_id}/regenerate",
    response_model=list[
        PersistedTestCaseResponse
    ],
)
def regenerate_test_cases(
    requirement_db_id: int,
    db: Session = Depends(get_db),
):

    requirement = get_requirement(
        db,
        requirement_db_id,
    )

    if requirement is None:
        raise HTTPException(
            status_code=404,
            detail="Requirement not found",
        )

    generated = (
        generate_test_cases_for_saved_requirement(
            db,
            requirement,
        )
    )

    delete_requirement_test_cases(
        db,
        requirement_db_id,
    )

    return save_test_cases(
        db,
        requirement_db_id,
        generated.test_cases,
    )


@router.patch(
    "/{test_case_db_id}/status",
    response_model=PersistedTestCaseResponse,
)
def update_test_case_status_endpoint(
    test_case_db_id: int,
    update: TestCaseStatusUpdate,
    db: Session = Depends(get_db),
):

    test_case = update_test_case_status(
        db,
        test_case_db_id,
        update.review_status,
    )

    if test_case is None:
        raise HTTPException(
            status_code=404,
            detail="Test case not found",
        )

    return test_case

@router.patch(
    "/{test_case_db_id}/execution-type",
    response_model=PersistedTestCaseResponse,
)
def update_test_case_execution_type_endpoint(
    test_case_db_id: int,
    update: TestCaseExecutionTypeUpdate,
    db: Session = Depends(get_db),
):

    test_case = (
        db.query(TestCaseDB)
        .filter(
            TestCaseDB.id ==
            test_case_db_id
        )
        .first()
    )


    if test_case is None:

        raise HTTPException(
            status_code=404,
            detail="Test case not found",
        )


    try:

        return (
            update_test_case_execution_type(
                db=db,
                test_case=test_case,
                execution_type=(
                    update.execution_type
                ),
            )
        )


    except ValueError as exc:

        raise HTTPException(
            status_code=409,
            detail=str(exc),
        ) from exc
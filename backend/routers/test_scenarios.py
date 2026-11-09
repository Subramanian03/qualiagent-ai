from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.db.database import get_db

from backend.models.test_scenario import (
    TestScenarioCreate,
    TestScenarioResponse,
)

from backend.services.test_scenario_service import (
    create_test_scenario,
    get_requirement,
    get_requirement_test_scenarios,
    get_scenario_by_business_id,
    get_test_scenario,
)

from backend.ai.errors import (
    AIProviderError,
)

from backend.services.scenario_generation_service import (
    generate_and_save_ai_scenarios,
)


router = APIRouter(
    prefix="/api/test-scenarios",
    tags=["Test Scenarios"]
)


@router.post(
    "/requirement/{requirement_db_id}",
    response_model=TestScenarioResponse,
    status_code=201
)

@router.post(
    "/requirement/{requirement_db_id}/generate",
    response_model=list[
        TestScenarioResponse
    ],
    status_code=201
)
def generate_requirement_scenarios(
    requirement_db_id: int,
    db: Session = Depends(get_db)
):

    requirement = get_requirement(
        db,
        requirement_db_id
    )

    if requirement is None:
        raise HTTPException(
            status_code=404,
            detail="Requirement not found"
        )


    existing_scenarios = (
        get_requirement_test_scenarios(
            db,
            requirement_db_id
        )
    )


    existing_ai_scenarios = [
        scenario
        for scenario in existing_scenarios
        if scenario.source == "ai"
    ]


    if existing_ai_scenarios:

        raise HTTPException(
            status_code=409,
            detail=(
                "AI scenarios already exist "
                "for this requirement"
            )
        )


    try:

        return (
            generate_and_save_ai_scenarios(
                db,
                requirement
            )
        )


    except AIProviderError as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc)
        ) from exc


    except ValueError as exc:

        db.rollback()

        raise HTTPException(
            status_code=409,
            detail=str(exc)
        ) from exc


    except IntegrityError as exc:

        db.rollback()

        raise HTTPException(
            status_code=409,
            detail=(
                "Scenario persistence "
                "conflict occurred"
            )
        ) from exc

def create_requirement_test_scenario(
    requirement_db_id: int,
    request: TestScenarioCreate,
    db: Session = Depends(get_db)
):

    requirement = get_requirement(
        db,
        requirement_db_id
    )

    if requirement is None:
        raise HTTPException(
            status_code=404,
            detail="Requirement not found"
        )


    existing = get_scenario_by_business_id(
        db,
        requirement_db_id,
        request.scenario_id
    )

    if existing is not None:
        raise HTTPException(
            status_code=409,
            detail=(
                "Scenario ID already exists "
                "for this requirement"
            )
        )


    try:

        return create_test_scenario(
            db,
            requirement_db_id,
            request
        )

    except IntegrityError as exc:

        db.rollback()

        raise HTTPException(
            status_code=409,
            detail=(
                "Scenario already exists "
                "for this requirement"
            )
        ) from exc


@router.get(
    "/requirement/{requirement_db_id}",
    response_model=list[
        TestScenarioResponse
    ]
)
def list_requirement_test_scenarios(
    requirement_db_id: int,
    db: Session = Depends(get_db)
):

    requirement = get_requirement(
        db,
        requirement_db_id
    )

    if requirement is None:
        raise HTTPException(
            status_code=404,
            detail="Requirement not found"
        )


    return get_requirement_test_scenarios(
        db,
        requirement_db_id
    )


@router.get(
    "/{scenario_db_id}",
    response_model=TestScenarioResponse
)
def read_test_scenario(
    scenario_db_id: int,
    db: Session = Depends(get_db)
):

    scenario = get_test_scenario(
        db,
        scenario_db_id
    )

    if scenario is None:
        raise HTTPException(
            status_code=404,
            detail="Test scenario not found"
        )


    return scenario
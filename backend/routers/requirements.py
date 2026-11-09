from fastapi import APIRouter

from backend.models.requirement import (
    RequirementAnalysisResponse,
    RequirementInput,
)
from backend.services.requirement_analyser import analyse_requirement

from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.db.database import get_db
from backend.models.requirement import (
    RequirementCreate,
    RequirementResponse,
)
from backend.services.project_service import get_project
from backend.services.requirement_service import (
    create_requirement,
    delete_requirement,
    get_project_requirements,
    get_requirement_by_business_id,
)
from backend.ai.errors import (
    AIProviderError,
)

from backend.models.ai_requirement_analysis import (
    AIRequirementAnalysis,
)

from backend.services.ai_requirement_analysis_service import (
    analyse_requirement_with_ai,
)


router = APIRouter(
    prefix="/api/requirements",
    tags=["Requirements"],
)


@router.post(
    "/analyse",
    response_model=AIRequirementAnalysis
)
def analyse_requirement_endpoint(
    request: RequirementCreate
):

    try:

        return analyse_requirement_with_ai(
            request
        )

    except AIProviderError as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc)
        ) from exc
def analyse_software_requirement(
    requirement: RequirementInput
) -> RequirementAnalysisResponse:
    return analyse_requirement(requirement)

@router.post(
    "/project/{project_id}",
    response_model=RequirementResponse,
    status_code=201
)
def create_project_requirement(
    project_id: int,
    requirement: RequirementCreate,
    db: Session = Depends(get_db)
):

    project = get_project(
        db,
        project_id
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    existing_requirement = get_requirement_by_business_id(
        db,
        project_id,
        requirement.requirement_id
    )

    if existing_requirement is not None:
        raise HTTPException(
            status_code=409,
            detail=(
                "Requirement ID already exists "
                "in this project"
            )
        )

    return create_requirement(
        db,
        project_id,
        requirement
    )


@router.get(
    "/project/{project_id}",
    response_model=list[RequirementResponse]
)
def list_project_requirements(
    project_id: int,
    db: Session = Depends(get_db)
):

    project = get_project(
        db,
        project_id
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return get_project_requirements(
        db,
        project_id
    )

@router.delete(
    "/{requirement_db_id}",
    status_code=204
)
def delete_requirement_endpoint(
    requirement_db_id: int,
    db: Session = Depends(get_db)
):

    requirement = delete_requirement(
        db,
        requirement_db_id
    )

    if requirement is None:
        raise HTTPException(
            status_code=404,
            detail="Requirement not found"
        )

    return None
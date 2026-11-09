from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.db.database import get_db
from backend.models.project import (
    ProjectCreate,
    ProjectResponse,
)
from backend.services.project_service import (
    create_project,
    get_project,
    get_projects,
)
from backend.models.cycle_readiness import (
    ProjectCycleReadiness,
)
from backend.services.cycle_readiness_service import (
    get_project_cycle_readiness,
)


router = APIRouter(
    prefix="/api/projects",
    tags=["Projects"]
)


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=201
)
def create_project_endpoint(
    project: ProjectCreate,
    db: Session = Depends(get_db)
):

    return create_project(
        db,
        project
    )


@router.get(
    "",
    response_model=list[ProjectResponse]
)
def get_projects_endpoint(
    db: Session = Depends(get_db)
):

    return get_projects(db)


@router.get(
    "/{project_id}",
    response_model=ProjectResponse
)
def get_project_endpoint(
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

    return project

@router.get(
    "/{project_id}/cycle-readiness",
    response_model=ProjectCycleReadiness,
)
def get_cycle_readiness_endpoint(
    project_id: int,
    db: Session = Depends(get_db),
):

    project = get_project(
        db,
        project_id
    )


    if project is None:

        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )


    try:

        return (
            get_project_cycle_readiness(
                db,
                project
            )
        )


    except ValueError as exc:

        raise HTTPException(
            status_code=409,
            detail=str(exc),
        ) from exc
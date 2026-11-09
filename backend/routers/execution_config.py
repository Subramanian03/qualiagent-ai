from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.db.database import get_db
from backend.models.execution_config import (
    ExecutionConfigResponse,
    ExecutionConfigUpsert,
)
from backend.services.execution_config_service import (
    get_execution_config,
    get_project,
    upsert_execution_config,
)


router = APIRouter(
    prefix="/api/execution-config",
    tags=["Execution Configuration"]
)


@router.put(
    "/project/{project_id}",
    response_model=ExecutionConfigResponse
)
def save_execution_config(
    project_id: int,
    request: ExecutionConfigUpsert,
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

    return upsert_execution_config(
        db,
        project_id,
        request
    )


@router.get(
    "/project/{project_id}",
    response_model=ExecutionConfigResponse
)
def read_execution_config(
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

    config = get_execution_config(
        db,
        project_id
    )

    if config is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Execution configuration "
                "not found"
            )
        )

    return config
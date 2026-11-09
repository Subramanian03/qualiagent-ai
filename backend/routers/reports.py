from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.db.database import get_db
from backend.db.project_model import (
    ProjectDB,
)
from backend.models.report import (
    ProjectQualitySummary,
    RequirementCoverage,
)
from backend.services.report_service import (
    get_project,
    get_project_quality_summary,
    get_requirement_coverage,
)

from backend.models.cycle_reporting import (
    ProjectCycleQualitySummary,
)

from backend.models.cycle_traceability import (
    ProjectCycleTraceability,
)

from backend.services.cycle_reporting_service import (
    get_project_cycle_quality_summary,
)

from backend.services.cycle_traceability_service import (
    get_project_cycle_traceability,
)
from backend.models.reporting_filters import (
    CycleReportingFilters,
)
from backend.models.release_quality import (
    ProjectReleaseQuality,
)
from backend.services.release_quality_service import (
    get_project_release_quality,
)


router = APIRouter(
    prefix="/api/reports",
    tags=["Reports"]
)


@router.get(
    "/project/{project_id}/summary",
    response_model=ProjectQualitySummary
)
def project_quality_summary(
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

    return get_project_quality_summary(
        db,
        project
    )

@router.get(
    "/project/{project_id}/coverage",
    response_model=list[
        RequirementCoverage
    ]
)
def project_requirement_coverage(
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

    return get_requirement_coverage(
        db,
        project_id
    )

@router.get(
    "/project/{project_id}/cycle-quality-summary",
    response_model=ProjectCycleQualitySummary
)
def get_project_cycle_quality_summary_endpoint(
    project_id: int,
    release: str | None = None,
    environment: str | None = None,
    cycle_status: str | None = None,
    result_status: str | None = None,
    execution_mode: str | None = None,
    db: Session = Depends(get_db)
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


    try:

        filters = CycleReportingFilters(
            release=release,
            environment=environment,
            cycle_status=cycle_status,
            result_status=result_status,
            execution_mode=execution_mode
        )


    except ValueError as exc:

        raise HTTPException(
            status_code=422,
            detail=str(exc)
        ) from exc

    return (
        get_project_cycle_quality_summary(
            db,
            project_id,
            filters
        )
    )

@router.get(
    "/project/{project_id}/cycle-traceability",
    response_model=ProjectCycleTraceability
)
def get_project_cycle_traceability_endpoint(
    project_id: int,
    release: str | None = None,
    environment: str | None = None,
    cycle_status: str | None = None,
    result_status: str | None = None,
    execution_mode: str | None = None,
    db: Session = Depends(get_db)
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
    try:

        filters = CycleReportingFilters(
            release=release,
            environment=environment,
            cycle_status=cycle_status,
            result_status=result_status,
            execution_mode=execution_mode
        )


    except ValueError as exc:

        raise HTTPException(
            status_code=422,
            detail=str(exc)
        ) from exc


    try:

        return (
            get_project_cycle_traceability(
                db,
                project_id,
                filters
            )
        )


    except ValueError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc)
        ) from exc

@router.get(
    "/project/{project_id}/release-quality",
    response_model=ProjectReleaseQuality
)
def get_project_release_quality_endpoint(
    project_id: int,
    release: str,
    environment: str | None = None,
    db: Session = Depends(get_db)
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


    try:

        return (
            get_project_release_quality(
                db,
                project_id=project_id,
                release=release,
                environment=environment
            )
        )


    except ValueError as exc:

        raise HTTPException(
            status_code=422,
            detail=str(exc)
        ) from exc
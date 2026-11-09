from sqlalchemy.orm import Session

from backend.db.project_model import ProjectDB
from backend.models.project import ProjectCreate


def create_project(
    db: Session,
    project: ProjectCreate
):

    db_project = ProjectDB(
        name=project.name,

        description=(
            project.description
        ),

        application_type=(
            project.application_type
        ),

        automation_engine=(
            project.automation_engine
        ),

        automation_language=(
            project.automation_language
        ),

        default_browser=(
            project.default_browser
        ),
    )


    try:

        db.add(
            db_project
        )

        db.commit()

        db.refresh(
            db_project
        )

        return db_project


    except Exception:

        db.rollback()

        raise
def get_projects(
    db: Session
):

    return (
        db.query(ProjectDB)
        .order_by(ProjectDB.id.desc())
        .all()
    )


def get_project(
    db: Session,
    project_id: int
):

    return (
        db.query(ProjectDB)
        .filter(
            ProjectDB.id == project_id
        )
        .first()
    )
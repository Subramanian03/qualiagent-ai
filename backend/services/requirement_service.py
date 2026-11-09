from sqlalchemy.orm import Session

from backend.db.requirement_model import RequirementDB
from backend.models.requirement import RequirementCreate


def create_requirement(
    db: Session,
    project_id: int,
    requirement: RequirementCreate
):

    db_requirement = RequirementDB(
        project_id=project_id,
        requirement_id=requirement.requirement_id,
        title=requirement.title,
        description=requirement.description,
        application_type=requirement.application_type
    )

    db.add(db_requirement)

    db.commit()

    db.refresh(db_requirement)

    return db_requirement


def get_project_requirements(
    db: Session,
    project_id: int
):

    return (
        db.query(RequirementDB)
        .filter(
            RequirementDB.project_id == project_id
        )
        .order_by(RequirementDB.id.asc())
        .all()
    )


def get_requirement(
    db: Session,
    requirement_db_id: int
):

    return (
        db.query(RequirementDB)
        .filter(
            RequirementDB.id == requirement_db_id
        )
        .first()
    )

def delete_requirement(
    db: Session,
    requirement_db_id: int
):

    requirement = get_requirement(
        db,
        requirement_db_id
    )

    if requirement is None:
        return None

    db.delete(requirement)

    db.commit()

    return requirement

def get_requirement_by_business_id(
    db: Session,
    project_id: int,
    requirement_id: str
):

    return (
        db.query(RequirementDB)
        .filter(
            RequirementDB.project_id == project_id,
            RequirementDB.requirement_id == requirement_id
        )
        .first()
    )
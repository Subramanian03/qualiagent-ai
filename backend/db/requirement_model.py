from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from backend.db.database import Base


class RequirementDB(Base):

    __tablename__ = "requirements"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    requirement_id: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id"),
        nullable=False
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    application_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    project = relationship(
        "ProjectDB",
        back_populates="requirements",
    )

    test_cases = relationship(
        "TestCaseDB",
        back_populates="requirement",
        cascade="all, delete-orphan"
    )

    test_scenarios = relationship(
    "TestScenarioDB",
    back_populates="requirement",
    cascade="all, delete-orphan"
    )
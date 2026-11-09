from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import JSON
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from backend.db.database import Base


class TestCaseDB(Base):

    __tablename__ = "test_cases"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    test_case_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    requirement_db_id: Mapped[int] = mapped_column(
        ForeignKey("requirements.id"),
        nullable=False
    )

    test_scenario_db_id: Mapped[
    int | None
] = mapped_column(
    ForeignKey(
        "test_scenarios.id"
    ),
    nullable=True,
    index=True
)

    requirement_id: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    test_scenario_db_id: Mapped[
    int | None
] = mapped_column(
    ForeignKey(
        "test_scenarios.id"
    ),
    nullable=True,
    index=True
)

    title: Mapped[str] = mapped_column(
        String(300),
        nullable=False
    )

    test_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    priority: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    preconditions: Mapped[list] = mapped_column(
        JSON,
        nullable=False
    )

    test_data: Mapped[list] = mapped_column(
        JSON,
        nullable=False
    )

    steps: Mapped[list] = mapped_column(
        JSON,
        nullable=False
    )

    automation_candidate: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False
    )

    execution_type: Mapped[str] = (
        mapped_column(
            String(20),
            nullable=False,
            default="manual"
        )
    )

    review_status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="draft"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    requirement = relationship(
        "RequirementDB",
        back_populates="test_cases"
    )

    test_scenario = relationship(
    "TestScenarioDB",
    back_populates="test_cases"
)

    automation_scripts = relationship(
    "AutomationScriptDB",
    back_populates="test_case",
    cascade="all, delete-orphan"
   )

    
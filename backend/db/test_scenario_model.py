from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from backend.db.database import Base


class TestScenarioDB(Base):

    __tablename__ = "test_scenarios"

    __table_args__ = (
        UniqueConstraint(
            "requirement_db_id",
            "scenario_id",
            name=(
                "uq_test_scenario_"
                "requirement_scenario_id"
            )
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    requirement_db_id: Mapped[int] = mapped_column(
        ForeignKey("requirements.id"),
        nullable=False,
        index=True
    )

    scenario_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    scenario_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="functional"
    )

    priority: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="medium"
    )

    source: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="ai"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


    requirement = relationship(
        "RequirementDB",
        back_populates="test_scenarios"
    )


    test_cases = relationship(
        "TestCaseDB",
        back_populates="test_scenario"
    )
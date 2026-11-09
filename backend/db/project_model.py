from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from backend.db.database import Base


class ProjectDB(Base):

    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        String(1000),
        nullable=False
    )

    application_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    automation_engine: Mapped[str] = (
        mapped_column(
            String(50),
            nullable=False,
            default="playwright"
        )
    )


    automation_language: Mapped[str] = (
        mapped_column(
            String(50),
            nullable=False,
            default="javascript"
        )
    )


    default_browser: Mapped[str] = (
        mapped_column(
            String(50),
            nullable=False,
            default="chromium"
        )
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    requirements = relationship(
        "RequirementDB",
        back_populates="project",
        cascade="all, delete-orphan"
    )

    execution_config = relationship(
    "ExecutionConfigDB",
    back_populates="project",
    uselist=False,
    cascade="all, delete-orphan"
)
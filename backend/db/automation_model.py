from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import JSON
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from backend.db.database import Base


class AutomationScriptDB(Base):

    __tablename__ = "automation_scripts"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    test_case_db_id: Mapped[int] = mapped_column(
        ForeignKey("test_cases.id"),
        nullable=False
    )

    framework: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="playwright"
    )

    language: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="javascript"
    )

    code: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default=""
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="draft"
    )

    version: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1
    )


    engine: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="playwright"
    )


    input_schema: Mapped[
        dict | None
    ] = mapped_column(
        JSON,
        nullable=True
    )


    source: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="ai_generated"
    )


    change_summary: Mapped[
        str | None
    ] = mapped_column(
        Text,
        nullable=True
    )


    parent_version_id: Mapped[
        int | None
    ] = mapped_column(
        ForeignKey(
            "automation_scripts.id"
        ),
        nullable=True
    )


    created_by: Mapped[
        int | None
    ] = mapped_column(
        Integer,
        nullable=True
    )


    reviewed_by: Mapped[
        int | None
    ] = mapped_column(
        Integer,
        nullable=True
    )


    reviewed_at: Mapped[
        datetime | None
    ] = mapped_column(
        DateTime,
        nullable=True
    )


    updated_at: Mapped[
        datetime | None
    ] = mapped_column(
        DateTime,
        nullable=True,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    test_case = relationship(
        "TestCaseDB",
        back_populates="automation_scripts"
    )

    executions = relationship(
        "ExecutionDB",
        back_populates="automation_script",
        cascade="all, delete-orphan"
    )

    parent_version = relationship(
        "AutomationScriptDB",
        remote_side=[
            id
        ],
        foreign_keys=[
            parent_version_id
        ],
        uselist=False
    )
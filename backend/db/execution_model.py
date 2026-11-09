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


class ExecutionDB(Base):

    __tablename__ = "executions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    automation_script_id: Mapped[int] = mapped_column(
        ForeignKey("automation_scripts.id"),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="pending"
    )

    started_at: Mapped[
        datetime | None
    ] = mapped_column(
        DateTime,
        nullable=True
    )

    completed_at: Mapped[
        datetime | None
    ] = mapped_column(
        DateTime,
        nullable=True
    )

    duration_ms: Mapped[
        int | None
    ] = mapped_column(
        Integer,
        nullable=True
    )

    exit_code: Mapped[
        int | None
    ] = mapped_column(
        Integer,
        nullable=True
    )

    stdout: Mapped[
        str | None
    ] = mapped_column(
        Text,
        nullable=True
    )

    stderr: Mapped[
        str | None
    ] = mapped_column(
        Text,
        nullable=True
    )

    error_message: Mapped[
        str | None
    ] = mapped_column(
        Text,
        nullable=True
    )

    screenshot_path: Mapped[
    str | None
] = mapped_column(
    Text,
    nullable=True
)

    trace_path: Mapped[
    str | None
] = mapped_column(
    Text,
    nullable=True
)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    automation_script = relationship(
        "AutomationScriptDB",
        back_populates="executions"
    )
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


class CycleTestItemDB(
    Base
):

    __tablename__ = (
        "cycle_test_items"
    )


    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )


    cycle_id: Mapped[int] = mapped_column(
        ForeignKey(
            "test_cycles.id"
        ),
        nullable=False,
        index=True
    )


    test_case_id: Mapped[int] = mapped_column(
        ForeignKey(
            "test_cases.id"
        ),
        nullable=False,
        index=True
    )


    execution_mode: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )


    automation_version_id: Mapped[
        int | None
    ] = mapped_column(
        ForeignKey(
            "automation_scripts.id"
        ),
        nullable=True,
        index=True
    )

    execution_id: Mapped[
        int | None
    ] = mapped_column(
        ForeignKey(
            "executions.id"
        ),
        nullable=True,
        index=True
    )


    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="not_run",
        index=True
    )


    position: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )


    actual_result: Mapped[
        str | None
    ] = mapped_column(
        Text,
        nullable=True
    )


    comment: Mapped[
        str | None
    ] = mapped_column(
        Text,
        nullable=True
    )


    defect_reference: Mapped[
        str | None
    ] = mapped_column(
        String(200),
        nullable=True
    )


    created_at: Mapped[
        datetime
    ] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )


    updated_at: Mapped[
        datetime | None
    ] = mapped_column(
        DateTime,
        nullable=True,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


    cycle = relationship(
        "TestCycleDB",
        back_populates="items"
    )


    test_case = relationship(
        "TestCaseDB"
    )


    automation_version = relationship(
        "AutomationScriptDB"
    )

    execution = relationship(
        "ExecutionDB"
    )

    @property
    def test_case_key(
        self
    ) -> str:

        if self.test_case is None:
            return str(
                self.test_case_id
            )

        return str(
            self.test_case.test_case_id
        )


    @property
    def test_case_title(
        self
    ) -> str:

        if self.test_case is None:
            return (
                "Unknown Test Case"
            )

        return str(
            self.test_case.title
        )


    @property
    def automation_version_number(
        self
    ) -> int | None:

        if self.automation_version is None:
            return None

        return (
            self.automation_version.version
        )


    @property
    def automation_engine(
        self
    ) -> str | None:

        if self.automation_version is None:
            return None

        return (
            self.automation_version.engine
            or
            self.automation_version.framework
        )


    @property
    def automation_language(
        self
    ) -> str | None:

        if self.automation_version is None:
            return None

        return (
            self.automation_version.language
        )
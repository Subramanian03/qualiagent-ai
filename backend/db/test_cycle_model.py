from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from backend.db.database import Base


class TestCycleDB(
    Base
):

    __tablename__ = "test_cycles"


    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )


    project_id: Mapped[int] = mapped_column(
        ForeignKey(
            "projects.id"
        ),
        nullable=False,
        index=True
    )


    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )


    release: Mapped[
        str | None
    ] = mapped_column(
        String(100),
        nullable=True
    )


    environment: Mapped[
        str | None
    ] = mapped_column(
        String(100),
        nullable=True
    )


    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="draft",
        index=True
    )


    created_at: Mapped[
        datetime
    ] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
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


    project = relationship(
        "ProjectDB"
    )


    items = relationship(
        "CycleTestItemDB",
        back_populates="cycle",
        cascade="all, delete-orphan",
        order_by="CycleTestItemDB.position"
    )
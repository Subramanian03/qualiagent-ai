from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from backend.db.database import Base


class ExecutionConfigDB(Base):

    __tablename__ = "execution_configs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id"),
        nullable=False,
        unique=True,
        index=True
    )

    environment_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="QA"
    )

    base_url: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    test_username: Mapped[
        str | None
    ] = mapped_column(
        String(255),
        nullable=True
    )

    test_first_name: Mapped[
        str | None
    ] = mapped_column(
        String(255),
        nullable=True
    )

    test_last_name: Mapped[
        str | None
    ] = mapped_column(
        String(255),
        nullable=True
    )

    test_postal_code: Mapped[
        str | None
    ] = mapped_column(
        String(50),
        nullable=True
    )

    credentials_required: Mapped[
        bool
    ] = mapped_column(
        Boolean,
        nullable=False,
        default=False
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

    project = relationship(
        "ProjectDB",
        back_populates="execution_config"
    )
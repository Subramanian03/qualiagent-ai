"""reconcile legacy schema

Revision ID: a6921deba322
Revises: c0d46243b1bc
Create Date: 2026-11-18 11:14:42.811174
"""

from typing import Sequence
from typing import Union

from alembic import op
import sqlalchemy as sa


# Revision identifiers used by Alembic.
revision: str = "a6921deba322"

down_revision: Union[
    str,
    Sequence[str],
    None
] = "c0d46243b1bc"

branch_labels: Union[
    str,
    Sequence[str],
    None
] = None

depends_on: Union[
    str,
    Sequence[str],
    None
] = None


def upgrade() -> None:
    """
    Reconcile legacy QualiAgent SQLite
    databases with the canonical baseline.

    Fresh databases created by Revision 1
    already contain these schema objects,
    so the operations below are conditional.
    """

    connection = (
        op.get_bind()
    )


    # -------------------------------------------------
    # 1. Ensure Test Case → Scenario lookup index exists.
    # -------------------------------------------------

    inspector = (
        sa.inspect(
            connection
        )
    )


    existing_indexes = {
        index["name"]
        for index
        in inspector.get_indexes(
            "test_cases"
        )
    }


    if (
        "ix_test_cases_test_scenario_db_id"
        not in existing_indexes
    ):

        op.create_index(
            "ix_test_cases_test_scenario_db_id",
            "test_cases",
            [
                "test_scenario_db_id"
            ],
            unique=False
        )


    # -------------------------------------------------
    # 2. Refresh reflection after schema modification.
    # -------------------------------------------------

    inspector = (
        sa.inspect(
            connection
        )
    )


    # -------------------------------------------------
    # 3. Ensure Automation parent-version FK exists.
    # -------------------------------------------------

    existing_foreign_keys = (
        inspector.get_foreign_keys(
            "automation_scripts"
        )
    )


    has_parent_foreign_key = any(
        (
            foreign_key.get(
                "constrained_columns"
            )
            ==
            [
                "parent_version_id"
            ]
            and
            foreign_key.get(
                "referred_table"
            )
            ==
            "automation_scripts"
            and
            foreign_key.get(
                "referred_columns"
            )
            ==
            [
                "id"
            ]
        )
        for foreign_key
        in existing_foreign_keys
    )


    if not has_parent_foreign_key:

        with op.batch_alter_table(
            "automation_scripts",
            schema=None,
            recreate="always"
        ) as batch_op:

            batch_op.create_foreign_key(
                (
                    "fk_automation_scripts_"
                    "parent_version"
                ),
                "automation_scripts",
                [
                    "parent_version_id"
                ],
                [
                    "id"
                ]
            )


def downgrade() -> None:
    """
    No-op by design.

    This revision reconciles historical
    SQLite databases with Revision 1's
    canonical schema.

    Revision 1 already creates the scenario
    index and parent-version foreign key on
    fresh databases. Removing those objects
    here could therefore make a fresh
    Revision-1 database inconsistent with
    its own canonical definition.
    """

    pass
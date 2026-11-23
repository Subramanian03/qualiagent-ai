"""initial QualiAgent schema baseline

Revision ID: c0d46243b1bc
Revises:
Create Date: 2026-11-18 10:33:27.150283
"""

from typing import Sequence
from typing import Union

from alembic import op
import sqlalchemy as sa


# Revision identifiers used by Alembic.
revision: str = "c0d46243b1bc"

down_revision: Union[
    str,
    Sequence[str],
    None
] = None

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
    """Create the complete QualiAgent schema."""

    op.create_table(
        "automation_scripts",

        sa.Column(
            "id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "test_case_db_id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "framework",
            sa.String(
                length=50
            ),
            nullable=False
        ),

        sa.Column(
            "language",
            sa.String(
                length=50
            ),
            nullable=False
        ),

        sa.Column(
            "code",
            sa.Text(),
            nullable=False
        ),

        sa.Column(
            "status",
            sa.String(
                length=20
            ),
            nullable=False
        ),

        sa.Column(
            "version",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "engine",
            sa.String(
                length=50
            ),
            nullable=False
        ),

        sa.Column(
            "input_schema",
            sa.JSON(),
            nullable=True
        ),

        sa.Column(
            "source",
            sa.String(
                length=30
            ),
            nullable=False
        ),

        sa.Column(
            "change_summary",
            sa.Text(),
            nullable=True
        ),

        sa.Column(
            "parent_version_id",
            sa.Integer(),
            nullable=True
        ),

        sa.Column(
            "source_execution_id",
            sa.Integer(),
            nullable=True
        ),

        sa.Column(
            "created_by",
            sa.Integer(),
            nullable=True
        ),

        sa.Column(
            "reviewed_by",
            sa.Integer(),
            nullable=True
        ),

        sa.Column(
            "reviewed_at",
            sa.DateTime(),
            nullable=True
        ),

        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False
        ),

        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False
        ),

        sa.ForeignKeyConstraint(
            [
                "parent_version_id"
            ],
            [
                "automation_scripts.id"
            ],
            name=(
                "fk_automation_scripts_"
                "parent_version"
            )
        ),

        sa.ForeignKeyConstraint(
            [
                "source_execution_id"
            ],
            [
                "executions.id"
            ]
        ),

        sa.ForeignKeyConstraint(
            [
                "test_case_db_id"
            ],
            [
                "test_cases.id"
            ]
        ),

        sa.PrimaryKeyConstraint(
            "id"
        )
    )


    with op.batch_alter_table(
        "automation_scripts",
        schema=None
    ) as batch_op:

        batch_op.create_index(
            batch_op.f(
                "ix_automation_scripts_id"
            ),
            [
                "id"
            ],
            unique=False
        )

        batch_op.create_index(
            "idx_automation_scripts_status",
            [
                "status"
            ],
            unique=False
        )

        batch_op.create_index(
            (
                "idx_automation_scripts_"
                "parent_version"
            ),
            [
                "parent_version_id"
            ],
            unique=False
        )

        batch_op.create_index(
            (
                "idx_automation_scripts_"
                "test_case_version"
            ),
            [
                "test_case_db_id",
                "version"
            ],
            unique=False
        )


    op.create_table(
        "executions",

        sa.Column(
            "id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "automation_script_id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "status",
            sa.String(
                length=20
            ),
            nullable=False
        ),

        sa.Column(
            "started_at",
            sa.DateTime(),
            nullable=True
        ),

        sa.Column(
            "completed_at",
            sa.DateTime(),
            nullable=True
        ),

        sa.Column(
            "duration_ms",
            sa.Integer(),
            nullable=True
        ),

        sa.Column(
            "exit_code",
            sa.Integer(),
            nullable=True
        ),

        sa.Column(
            "stdout",
            sa.Text(),
            nullable=True
        ),

        sa.Column(
            "stderr",
            sa.Text(),
            nullable=True
        ),

        sa.Column(
            "error_message",
            sa.Text(),
            nullable=True
        ),

        sa.Column(
            "screenshot_path",
            sa.Text(),
            nullable=True
        ),

        sa.Column(
            "trace_path",
            sa.Text(),
            nullable=True
        ),

        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False
        ),

        sa.ForeignKeyConstraint(
            [
                "automation_script_id"
            ],
            [
                "automation_scripts.id"
            ]
        ),

        sa.PrimaryKeyConstraint(
            "id"
        )
    )


    with op.batch_alter_table(
        "executions",
        schema=None
    ) as batch_op:

        batch_op.create_index(
            batch_op.f(
                "ix_executions_id"
            ),
            [
                "id"
            ],
            unique=False
        )


    op.create_table(
        "projects",

        sa.Column(
            "id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "name",
            sa.String(
                length=200
            ),
            nullable=False
        ),

        sa.Column(
            "description",
            sa.String(
                length=1000
            ),
            nullable=False
        ),

        sa.Column(
            "application_type",
            sa.String(
                length=20
            ),
            nullable=False
        ),

        sa.Column(
            "automation_engine",
            sa.String(
                length=50
            ),
            nullable=False
        ),

        sa.Column(
            "automation_language",
            sa.String(
                length=50
            ),
            nullable=False
        ),

        sa.Column(
            "default_browser",
            sa.String(
                length=50
            ),
            nullable=False
        ),

        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False
        ),

        sa.PrimaryKeyConstraint(
            "id"
        )
    )


    with op.batch_alter_table(
        "projects",
        schema=None
    ) as batch_op:

        batch_op.create_index(
            batch_op.f(
                "ix_projects_id"
            ),
            [
                "id"
            ],
            unique=False
        )


    op.create_table(
        "execution_configs",

        sa.Column(
            "id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "project_id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "environment_name",
            sa.String(
                length=100
            ),
            nullable=False
        ),

        sa.Column(
            "base_url",
            sa.String(
                length=500
            ),
            nullable=False
        ),

        sa.Column(
            "test_username",
            sa.String(
                length=255
            ),
            nullable=True
        ),

        sa.Column(
            "test_first_name",
            sa.String(
                length=255
            ),
            nullable=True
        ),

        sa.Column(
            "test_last_name",
            sa.String(
                length=255
            ),
            nullable=True
        ),

        sa.Column(
            "test_postal_code",
            sa.String(
                length=50
            ),
            nullable=True
        ),

        sa.Column(
            "credentials_required",
            sa.Boolean(),
            nullable=False
        ),

        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False
        ),

        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False
        ),

        sa.ForeignKeyConstraint(
            [
                "project_id"
            ],
            [
                "projects.id"
            ]
        ),

        sa.PrimaryKeyConstraint(
            "id"
        )
    )


    with op.batch_alter_table(
        "execution_configs",
        schema=None
    ) as batch_op:

        batch_op.create_index(
            batch_op.f(
                "ix_execution_configs_id"
            ),
            [
                "id"
            ],
            unique=False
        )

        batch_op.create_index(
            batch_op.f(
                "ix_execution_configs_project_id"
            ),
            [
                "project_id"
            ],
            unique=True
        )


    op.create_table(
        "requirements",

        sa.Column(
            "id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "requirement_id",
            sa.String(
                length=50
            ),
            nullable=False
        ),

        sa.Column(
            "project_id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "title",
            sa.String(
                length=200
            ),
            nullable=False
        ),

        sa.Column(
            "description",
            sa.Text(),
            nullable=False
        ),

        sa.Column(
            "application_type",
            sa.String(
                length=20
            ),
            nullable=False
        ),

        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False
        ),

        sa.ForeignKeyConstraint(
            [
                "project_id"
            ],
            [
                "projects.id"
            ]
        ),

        sa.PrimaryKeyConstraint(
            "id"
        )
    )


    with op.batch_alter_table(
        "requirements",
        schema=None
    ) as batch_op:

        batch_op.create_index(
            batch_op.f(
                "ix_requirements_id"
            ),
            [
                "id"
            ],
            unique=False
        )


    op.create_table(
        "test_cycles",

        sa.Column(
            "id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "project_id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "name",
            sa.String(
                length=200
            ),
            nullable=False
        ),

        sa.Column(
            "release",
            sa.String(
                length=100
            ),
            nullable=True
        ),

        sa.Column(
            "environment",
            sa.String(
                length=100
            ),
            nullable=True
        ),

        sa.Column(
            "status",
            sa.String(
                length=30
            ),
            nullable=False
        ),

        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False
        ),

        sa.Column(
            "started_at",
            sa.DateTime(),
            nullable=True
        ),

        sa.Column(
            "completed_at",
            sa.DateTime(),
            nullable=True
        ),

        sa.ForeignKeyConstraint(
            [
                "project_id"
            ],
            [
                "projects.id"
            ]
        ),

        sa.PrimaryKeyConstraint(
            "id"
        )
    )


    with op.batch_alter_table(
        "test_cycles",
        schema=None
    ) as batch_op:

        batch_op.create_index(
            "idx_test_cycles_project",
            [
                "project_id"
            ],
            unique=False
        )

        batch_op.create_index(
            "idx_test_cycles_status",
            [
                "status"
            ],
            unique=False
        )


    op.create_table(
        "test_scenarios",

        sa.Column(
            "id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "requirement_db_id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "scenario_id",
            sa.String(
                length=100
            ),
            nullable=False
        ),

        sa.Column(
            "title",
            sa.String(
                length=255
            ),
            nullable=False
        ),

        sa.Column(
            "description",
            sa.Text(),
            nullable=True
        ),

        sa.Column(
            "scenario_type",
            sa.String(
                length=50
            ),
            nullable=False
        ),

        sa.Column(
            "priority",
            sa.String(
                length=20
            ),
            nullable=False
        ),

        sa.Column(
            "source",
            sa.String(
                length=30
            ),
            nullable=False
        ),

        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False
        ),

        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False
        ),

        sa.ForeignKeyConstraint(
            [
                "requirement_db_id"
            ],
            [
                "requirements.id"
            ]
        ),

        sa.PrimaryKeyConstraint(
            "id"
        ),

        sa.UniqueConstraint(
            "requirement_db_id",
            "scenario_id",
            name=(
                "uq_test_scenario_"
                "requirement_scenario_id"
            )
        )
    )


    with op.batch_alter_table(
        "test_scenarios",
        schema=None
    ) as batch_op:

        batch_op.create_index(
            batch_op.f(
                "ix_test_scenarios_id"
            ),
            [
                "id"
            ],
            unique=False
        )

        batch_op.create_index(
            batch_op.f(
                "ix_test_scenarios_requirement_db_id"
            ),
            [
                "requirement_db_id"
            ],
            unique=False
        )


    op.create_table(
        "test_cases",

        sa.Column(
            "id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "test_case_id",
            sa.String(
                length=100
            ),
            nullable=False
        ),

        sa.Column(
            "requirement_db_id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "test_scenario_db_id",
            sa.Integer(),
            nullable=True
        ),

        sa.Column(
            "requirement_id",
            sa.String(
                length=50
            ),
            nullable=False
        ),

        sa.Column(
            "title",
            sa.String(
                length=300
            ),
            nullable=False
        ),

        sa.Column(
            "test_type",
            sa.String(
                length=50
            ),
            nullable=False
        ),

        sa.Column(
            "priority",
            sa.String(
                length=20
            ),
            nullable=False
        ),

        sa.Column(
            "preconditions",
            sa.JSON(),
            nullable=False
        ),

        sa.Column(
            "test_data",
            sa.JSON(),
            nullable=False
        ),

        sa.Column(
            "steps",
            sa.JSON(),
            nullable=False
        ),

        sa.Column(
            "automation_candidate",
            sa.Boolean(),
            nullable=False
        ),

        sa.Column(
            "execution_type",
            sa.String(
                length=20
            ),
            nullable=False
        ),

        sa.Column(
            "review_status",
            sa.String(
                length=20
            ),
            nullable=False
        ),

        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False
        ),

        sa.ForeignKeyConstraint(
            [
                "requirement_db_id"
            ],
            [
                "requirements.id"
            ]
        ),

        sa.ForeignKeyConstraint(
            [
                "test_scenario_db_id"
            ],
            [
                "test_scenarios.id"
            ]
        ),

        sa.PrimaryKeyConstraint(
            "id"
        )
    )


    with op.batch_alter_table(
        "test_cases",
        schema=None
    ) as batch_op:

        batch_op.create_index(
            batch_op.f(
                "ix_test_cases_id"
            ),
            [
                "id"
            ],
            unique=False
        )

        batch_op.create_index(
            batch_op.f(
                "ix_test_cases_test_scenario_db_id"
            ),
            [
                "test_scenario_db_id"
            ],
            unique=False
        )


    op.create_table(
        "cycle_test_items",

        sa.Column(
            "id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "cycle_id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "test_case_id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "execution_mode",
            sa.String(
                length=20
            ),
            nullable=False
        ),

        sa.Column(
            "automation_version_id",
            sa.Integer(),
            nullable=True
        ),

        sa.Column(
            "execution_id",
            sa.Integer(),
            nullable=True
        ),

        sa.Column(
            "status",
            sa.String(
                length=30
            ),
            nullable=False
        ),

        sa.Column(
            "position",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "actual_result",
            sa.Text(),
            nullable=True
        ),

        sa.Column(
            "comment",
            sa.Text(),
            nullable=True
        ),

        sa.Column(
            "defect_reference",
            sa.String(
                length=200
            ),
            nullable=True
        ),

        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False
        ),

        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=True
        ),

        sa.ForeignKeyConstraint(
            [
                "automation_version_id"
            ],
            [
                "automation_scripts.id"
            ]
        ),

        sa.ForeignKeyConstraint(
            [
                "cycle_id"
            ],
            [
                "test_cycles.id"
            ]
        ),

        sa.ForeignKeyConstraint(
            [
                "execution_id"
            ],
            [
                "executions.id"
            ]
        ),

        sa.ForeignKeyConstraint(
            [
                "test_case_id"
            ],
            [
                "test_cases.id"
            ]
        ),

        sa.PrimaryKeyConstraint(
            "id"
        )
    )


    with op.batch_alter_table(
        "cycle_test_items",
        schema=None
    ) as batch_op:

        batch_op.create_index(
            "idx_cycle_items_automation",
            [
                "automation_version_id"
            ],
            unique=False
        )

        batch_op.create_index(
            "idx_cycle_items_cycle",
            [
                "cycle_id"
            ],
            unique=False
        )

        batch_op.create_index(
            "idx_cycle_items_execution",
            [
                "execution_id"
            ],
            unique=False
        )

        batch_op.create_index(
            "idx_cycle_items_status",
            [
                "status"
            ],
            unique=False
        )

        batch_op.create_index(
            "idx_cycle_items_test_case",
            [
                "test_case_id"
            ],
            unique=False
        )


def downgrade() -> None:
    """Remove the complete QualiAgent schema."""

    with op.batch_alter_table(
        "cycle_test_items",
        schema=None
    ) as batch_op:

        batch_op.drop_index(
            "idx_cycle_items_test_case"
        )

        batch_op.drop_index(
            "idx_cycle_items_status"
        )

        batch_op.drop_index(
            "idx_cycle_items_execution"
        )

        batch_op.drop_index(
            "idx_cycle_items_cycle"
        )

        batch_op.drop_index(
            "idx_cycle_items_automation"
        )


    op.drop_table(
        "cycle_test_items"
    )


    with op.batch_alter_table(
        "test_cases",
        schema=None
    ) as batch_op:

        batch_op.drop_index(
            batch_op.f(
                "ix_test_cases_test_scenario_db_id"
            )
        )

        batch_op.drop_index(
            batch_op.f(
                "ix_test_cases_id"
            )
        )


    op.drop_table(
        "test_cases"
    )


    with op.batch_alter_table(
        "test_scenarios",
        schema=None
    ) as batch_op:

        batch_op.drop_index(
            batch_op.f(
                "ix_test_scenarios_requirement_db_id"
            )
        )

        batch_op.drop_index(
            batch_op.f(
                "ix_test_scenarios_id"
            )
        )


    op.drop_table(
        "test_scenarios"
    )


    with op.batch_alter_table(
        "test_cycles",
        schema=None
    ) as batch_op:

        batch_op.drop_index(
            "idx_test_cycles_status"
        )

        batch_op.drop_index(
            "idx_test_cycles_project"
        )


    op.drop_table(
        "test_cycles"
    )


    with op.batch_alter_table(
        "requirements",
        schema=None
    ) as batch_op:

        batch_op.drop_index(
            batch_op.f(
                "ix_requirements_id"
            )
        )


    op.drop_table(
        "requirements"
    )


    with op.batch_alter_table(
        "execution_configs",
        schema=None
    ) as batch_op:

        batch_op.drop_index(
            batch_op.f(
                "ix_execution_configs_project_id"
            )
        )

        batch_op.drop_index(
            batch_op.f(
                "ix_execution_configs_id"
            )
        )


    op.drop_table(
        "execution_configs"
    )


    with op.batch_alter_table(
        "projects",
        schema=None
    ) as batch_op:

        batch_op.drop_index(
            batch_op.f(
                "ix_projects_id"
            )
        )


    op.drop_table(
        "projects"
    )


    with op.batch_alter_table(
        "executions",
        schema=None
    ) as batch_op:

        batch_op.drop_index(
            batch_op.f(
                "ix_executions_id"
            )
        )


    op.drop_table(
        "executions"
    )


    with op.batch_alter_table(
        "automation_scripts",
        schema=None
    ) as batch_op:

        batch_op.drop_index(
            (
                "idx_automation_scripts_"
                "test_case_version"
            )
        )

        batch_op.drop_index(
            (
                "idx_automation_scripts_"
                "parent_version"
            )
        )

        batch_op.drop_index(
            "idx_automation_scripts_status"
        )

        batch_op.drop_index(
            batch_op.f(
                "ix_automation_scripts_id"
            )
        )


    op.drop_table(
        "automation_scripts"
    )
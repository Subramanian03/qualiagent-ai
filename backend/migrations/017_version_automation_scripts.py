import sqlite3

from pathlib import Path


PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parents[2]
)


DATABASE_PATH = (
    PROJECT_ROOT /
    "storage" /
    "qualiagent.db"
)


TARGET_COLUMNS = {
    "version": (
        "INTEGER NOT NULL DEFAULT 1"
    ),

    "engine": (
        "TEXT NOT NULL DEFAULT 'playwright'"
    ),

    "input_schema": (
        "TEXT"
    ),

    "source": (
        "TEXT NOT NULL "
        "DEFAULT 'ai_generated'"
    ),

    "change_summary": (
        "TEXT"
    ),

    "parent_version_id": (
        "INTEGER"
    ),

    "created_by": (
        "INTEGER"
    ),

    "reviewed_by": (
        "INTEGER"
    ),

    "reviewed_at": (
        "DATETIME"
    ),

    "updated_at": (
        "DATETIME"
    ),
}


def get_columns(
    connection
) -> set[str]:

    rows = connection.execute(
        """
        PRAGMA table_info(
            automation_scripts
        )
        """
    ).fetchall()

    return {
        row[1]
        for row in rows
    }


def migrate():

    if not DATABASE_PATH.exists():

        raise RuntimeError(
            "QualiAgent database not found: "
            f"{DATABASE_PATH}"
        )


    connection = sqlite3.connect(
        DATABASE_PATH
    )


    try:

        connection.execute(
            "PRAGMA foreign_keys = ON"
        )


        table_exists = (
            connection.execute(
                """
                SELECT name
                FROM sqlite_master
                WHERE
                    type = 'table'
                    AND name =
                        'automation_scripts'
                """
            ).fetchone()
        )


        if table_exists is None:

            raise RuntimeError(
                "automation_scripts table "
                "does not exist"
            )


        existing_columns = get_columns(
            connection
        )


        print(
            "Existing columns:",
            sorted(existing_columns)
        )


        connection.execute(
            "BEGIN IMMEDIATE"
        )


        for (
            column_name,
            column_definition
        ) in TARGET_COLUMNS.items():

            if (
                column_name
                in existing_columns
            ):

                print(
                    f"SKIP: {column_name} "
                    "already exists"
                )

                continue


            sql = (
                "ALTER TABLE "
                "automation_scripts "
                f"ADD COLUMN {column_name} "
                f"{column_definition}"
            )


            print(
                f"ADD: {column_name}"
            )

            connection.execute(
                sql
            )


        # Existing records are version 1.
        # Preserve existing source as legacy
        # rather than pretending those rows
        # belong to the new versioning flow.

        connection.execute(
            """
            UPDATE automation_scripts
            SET version = 1
            WHERE version IS NULL
            """
        )


        connection.execute(
            """
            UPDATE automation_scripts
            SET engine = 'playwright'
            WHERE
                engine IS NULL
                OR TRIM(engine) = ''
            """
        )


        connection.execute(
            """
            UPDATE automation_scripts
            SET source = 'legacy'
            WHERE
                source IS NULL
                OR TRIM(source) = ''
                OR source = 'ai_generated'
            """
        )


        connection.execute(
            """
            UPDATE automation_scripts
            SET updated_at =
                CURRENT_TIMESTAMP
            WHERE updated_at IS NULL
            """
        )


        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_automation_scripts_test_case_version
            ON automation_scripts(
                test_case_db_id,
                version
            )
            """
        )


        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_automation_scripts_parent_version
            ON automation_scripts(
                parent_version_id
            )
            """
        )


        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_automation_scripts_status
            ON automation_scripts(
                status
            )
            """
        )


        connection.commit()


        final_columns = get_columns(
            connection
        )


        print(
            "\nMigration successful."
        )

        print(
            "Final columns:",
            sorted(final_columns)
        )


    except Exception:

        connection.rollback()

        raise


    finally:

        connection.close()


if __name__ == "__main__":

    migrate()
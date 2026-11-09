import sqlite3

from pathlib import Path


PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parents[2]
)


DATABASE_PATH = (
    PROJECT_ROOT
    / "storage"
    / "qualiagent.db"
)


TARGET_COLUMNS = {
    "automation_engine": (
        "TEXT NOT NULL "
        "DEFAULT 'playwright'"
    ),
    "automation_language": (
        "TEXT NOT NULL "
        "DEFAULT 'javascript'"
    ),
    "default_browser": (
        "TEXT NOT NULL "
        "DEFAULT 'chromium'"
    ),
}


def get_columns(connection):
    rows = connection.execute(
        "PRAGMA table_info(projects)"
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
        table_exists = (
            connection.execute(
                """
                SELECT name
                FROM sqlite_master
                WHERE
                    type = 'table'
                    AND name = 'projects'
                """
            ).fetchone()
        )

        if table_exists is None:
            raise RuntimeError(
                "projects table does not exist"
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

            if column_name in existing_columns:
                print(
                    f"SKIP: {column_name} "
                    "already exists"
                )
                continue

            print(
                f"ADD: {column_name}"
            )

            connection.execute(
                "ALTER TABLE projects "
                f"ADD COLUMN {column_name} "
                f"{column_definition}"
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
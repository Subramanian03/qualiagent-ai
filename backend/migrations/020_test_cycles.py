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


def table_exists(
    connection,
    table_name
):

    return (
        connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE
                type = 'table'
                AND name = ?
            """,
            (
                table_name,
            )
        ).fetchone()
        is not None
    )


def migrate():

    if not DATABASE_PATH.exists():

        raise RuntimeError(
            "QualiAgent database "
            f"not found: {DATABASE_PATH}"
        )


    connection = sqlite3.connect(
        DATABASE_PATH
    )


    try:

        connection.execute(
            "PRAGMA foreign_keys = ON"
        )


        connection.execute(
            "BEGIN IMMEDIATE"
        )


        if not table_exists(
            connection,
            "test_cycles"
        ):

            print(
                "CREATE: test_cycles"
            )


            connection.execute(
                """
                CREATE TABLE test_cycles (
                    id INTEGER
                        PRIMARY KEY
                        AUTOINCREMENT,

                    project_id INTEGER
                        NOT NULL,

                    name TEXT
                        NOT NULL,

                    release TEXT,

                    environment TEXT,

                    status TEXT
                        NOT NULL
                        DEFAULT 'draft',

                    created_at DATETIME
                        NOT NULL
                        DEFAULT CURRENT_TIMESTAMP,

                    started_at DATETIME,

                    completed_at DATETIME,

                    FOREIGN KEY(project_id)
                        REFERENCES projects(id)
                )
                """
            )


        else:

            print(
                "SKIP: test_cycles exists"
            )


        if not table_exists(
            connection,
            "cycle_test_items"
        ):

            print(
                "CREATE: cycle_test_items"
            )


            connection.execute(
                """
                CREATE TABLE cycle_test_items (
                    id INTEGER
                        PRIMARY KEY
                        AUTOINCREMENT,

                    cycle_id INTEGER
                        NOT NULL,

                    test_case_id INTEGER
                        NOT NULL,

                    execution_mode TEXT
                        NOT NULL,

                    automation_version_id
                        INTEGER,

                    status TEXT
                        NOT NULL
                        DEFAULT 'not_run',

                    position INTEGER
                        NOT NULL
                        DEFAULT 0,

                    actual_result TEXT,

                    comment TEXT,

                    defect_reference TEXT,

                    created_at DATETIME
                        NOT NULL
                        DEFAULT CURRENT_TIMESTAMP,

                    updated_at DATETIME,

                    FOREIGN KEY(cycle_id)
                        REFERENCES test_cycles(id),

                    FOREIGN KEY(test_case_id)
                        REFERENCES test_cases(id),

                    FOREIGN KEY(
                        automation_version_id
                    )
                        REFERENCES
                        automation_scripts(id)
                )
                """
            )


        else:

            print(
                "SKIP: cycle_test_items exists"
            )


        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_test_cycles_project
            ON test_cycles(project_id)
            """
        )


        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_test_cycles_status
            ON test_cycles(status)
            """
        )


        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_cycle_items_cycle
            ON cycle_test_items(cycle_id)
            """
        )


        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_cycle_items_test_case
            ON cycle_test_items(test_case_id)
            """
        )


        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_cycle_items_automation
            ON cycle_test_items(
                automation_version_id
            )
            """
        )


        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_cycle_items_status
            ON cycle_test_items(status)
            """
        )


        connection.commit()


        print(
            "\nTest Cycle migration "
            "successful."
        )


    except Exception:

        connection.rollback()

        raise


    finally:

        connection.close()


if __name__ == "__main__":

    migrate()
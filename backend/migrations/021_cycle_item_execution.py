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


def get_columns(
    connection
):

    return {
        row[1]
        for row in connection.execute(
            """
            PRAGMA table_info(
                cycle_test_items
            )
            """
        ).fetchall()
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


        columns = get_columns(
            connection
        )


        connection.execute(
            "BEGIN IMMEDIATE"
        )


        if "execution_id" not in columns:

            print(
                "ADD: execution_id"
            )


            connection.execute(
                """
                ALTER TABLE
                    cycle_test_items
                ADD COLUMN
                    execution_id INTEGER
                    REFERENCES executions(id)
                """
            )


        else:

            print(
                "SKIP: execution_id "
                "already exists"
            )


        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_cycle_items_execution
            ON cycle_test_items(
                execution_id
            )
            """
        )


        connection.commit()


        print(
            "\nCycle execution linkage "
            "migration successful."
        )


    except Exception:

        connection.rollback()

        raise


    finally:

        connection.close()


if __name__ == "__main__":

    migrate()
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
    rows = connection.execute(
        "PRAGMA table_info(test_cases)"
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
                    AND name = 'test_cases'
                """
            ).fetchone()
        )


        if table_exists is None:

            raise RuntimeError(
                "test_cases table does "
                "not exist"
            )


        columns = get_columns(
            connection
        )


        print(
            "Existing columns:",
            sorted(columns)
        )


        connection.execute(
            "BEGIN IMMEDIATE"
        )


        if (
            "execution_type"
            not in columns
        ):

            print(
                "ADD: execution_type"
            )

            connection.execute(
                """
                ALTER TABLE test_cases
                ADD COLUMN execution_type
                TEXT NOT NULL
                DEFAULT 'manual'
                """
            )

        else:

            print(
                "SKIP: execution_type "
                "already exists"
            )


        connection.execute(
            """
            UPDATE test_cases
            SET execution_type = 'manual'
            WHERE
                execution_type IS NULL
                OR TRIM(execution_type) = ''
                OR LOWER(execution_type)
                    NOT IN (
                        'manual',
                        'automation',
                        'both'
                    )
            """
        )


        connection.commit()


        print(
            "\nMigration successful."
        )


        counts = connection.execute(
            """
            SELECT
                execution_type,
                COUNT(*)
            FROM test_cases
            GROUP BY execution_type
            ORDER BY execution_type
            """
        ).fetchall()


        print(
            "Execution type counts:",
            counts
        )


    except Exception:

        connection.rollback()

        raise


    finally:

        connection.close()


if __name__ == "__main__":

    migrate()
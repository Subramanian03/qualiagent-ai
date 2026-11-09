import sqlite3


DATABASE_PATH = "storage/qualiagent.db"


def get_columns(
    connection,
    table_name
):
    rows = connection.execute(
        f"PRAGMA table_info({table_name})"
    ).fetchall()

    return {
        row[1]
        for row in rows
    }


def run_migration():
    connection = sqlite3.connect(
        DATABASE_PATH
    )

    try:
        columns = get_columns(
            connection,
            "executions"
        )

        if "screenshot_path" not in columns:

            connection.execute(
                """
                ALTER TABLE executions
                ADD COLUMN screenshot_path TEXT
                """
            )

            print(
                "screenshot_path added"
            )

        if "trace_path" not in columns:

            connection.execute(
                """
                ALTER TABLE executions
                ADD COLUMN trace_path TEXT
                """
            )

            print(
                "trace_path added"
            )

        connection.commit()

        print(
            "Execution evidence migration complete"
        )

    finally:
        connection.close()


if __name__ == "__main__":
    run_migration()
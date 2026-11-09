import sqlite3


DATABASE_PATH = "storage/qualiagent.db"


def column_exists(
    connection,
    table_name,
    column_name
):
    cursor = connection.execute(
        f"PRAGMA table_info({table_name})"
    )

    columns = [
        row[1]
        for row in cursor.fetchall()
    ]

    return column_name in columns


def run_migration():
    connection = sqlite3.connect(
        DATABASE_PATH
    )

    try:
        if column_exists(
            connection,
            "test_cases",
            "review_status"
        ):
            print(
                "review_status column already exists"
            )
            return

        connection.execute(
            """
            ALTER TABLE test_cases
            ADD COLUMN review_status
            VARCHAR(20)
            NOT NULL
            DEFAULT 'draft'
            """
        )

        connection.commit()

        print(
            "review_status column added successfully"
        )

    finally:
        connection.close()


if __name__ == "__main__":
    run_migration()
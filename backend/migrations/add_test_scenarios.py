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
            "test_cases"
        )

        if (
            "test_scenario_db_id"
            not in columns
        ):

            connection.execute(
                """
                ALTER TABLE test_cases
                ADD COLUMN
                test_scenario_db_id INTEGER
                REFERENCES test_scenarios(id)
                """
            )

            print(
                "test_scenario_db_id added"
            )

        else:

            print(
                "test_scenario_db_id "
                "already exists"
            )


        connection.commit()

        print(
            "Migration complete"
        )

    finally:

        connection.close()


if __name__ == "__main__":
    run_migration()
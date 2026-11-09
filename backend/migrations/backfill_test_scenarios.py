import sqlite3


DATABASE_PATH = "storage/qualiagent.db"


def run_backfill():

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.row_factory = (
        sqlite3.Row
    )

    try:

        requirements = (
            connection.execute(
                """
                SELECT DISTINCT
                    r.id,
                    r.requirement_id,
                    r.title
                FROM requirements r
                INNER JOIN test_cases tc
                    ON tc.requirement_db_id
                    = r.id
                WHERE tc.test_scenario_db_id
                    IS NULL
                """
            )
            .fetchall()
        )


        for requirement in requirements:

            scenario_id = (
                f"{requirement['requirement_id']}"
                "-SCN-LEGACY"
            )


            existing = (
                connection.execute(
                    """
                    SELECT id
                    FROM test_scenarios
                    WHERE requirement_db_id = ?
                      AND scenario_id = ?
                    """,
                    (
                        requirement["id"],
                        scenario_id
                    )
                )
                .fetchone()
            )


            if existing:

                scenario_db_id = (
                    existing["id"]
                )

            else:

                cursor = connection.execute(
                    """
                    INSERT INTO test_scenarios
                    (
                        requirement_db_id,
                        scenario_id,
                        title,
                        description,
                        scenario_type,
                        priority,
                        source,
                        created_at,
                        updated_at
                    )
                    VALUES
                    (
                        ?,
                        ?,
                        ?,
                        ?,
                        'functional',
                        'medium',
                        'legacy',
                        CURRENT_TIMESTAMP,
                        CURRENT_TIMESTAMP
                    )
                    """,
                    (
                        requirement["id"],
                        scenario_id,
                        (
                            "Legacy tests for "
                            + requirement["title"]
                        ),
                        (
                            "Compatibility scenario "
                            "for existing test cases."
                        )
                    )
                )

                scenario_db_id = (
                    cursor.lastrowid
                )


            connection.execute(
                """
                UPDATE test_cases

                SET test_scenario_db_id = ?

                WHERE requirement_db_id = ?
                  AND test_scenario_db_id
                    IS NULL
                """,
                (
                    scenario_db_id,
                    requirement["id"]
                )
            )


        connection.commit()

        print(
            "Existing test cases "
            "linked to legacy scenarios"
        )

    finally:

        connection.close()


if __name__ == "__main__":
    run_backfill()
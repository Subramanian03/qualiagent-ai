from sqlalchemy.orm import Session

from backend.db.test_case_model import TestCaseDB
from backend.models.test_case import TestCase
from backend.models.ai_test_case_generation import (
    AITestCaseGeneration,
)


def save_test_cases(
    db: Session,
    requirement_db_id: int,
    test_cases: list[TestCase]
):

    saved_test_cases = []

    for test_case in test_cases:

        db_test_case = TestCaseDB(
            test_case_id=test_case.test_case_id,
            requirement_db_id=requirement_db_id,
            requirement_id=test_case.requirement_id,
            title=test_case.title,
            test_type=test_case.test_type,
            priority=test_case.priority,
            preconditions=test_case.preconditions,
            test_data=test_case.test_data,
            steps=[
                step.model_dump()
                for step in test_case.steps
            ],
            automation_candidate=(
                test_case.automation_candidate
            )
        )

        db.add(db_test_case)

        saved_test_cases.append(
            db_test_case
        )

    db.commit()

    for test_case in saved_test_cases:
        db.refresh(test_case)

    return saved_test_cases


def get_requirement_test_cases(
    db: Session,
    requirement_db_id: int
):

    return (
        db.query(TestCaseDB)
        .filter(
            TestCaseDB.requirement_db_id
            == requirement_db_id
        )
        .order_by(TestCaseDB.id.asc())
        .all()
    )

def delete_requirement_test_cases(
    db: Session,
    requirement_db_id: int
):

    test_cases = get_requirement_test_cases(
        db,
        requirement_db_id
    )

    for test_case in test_cases:
        db.delete(test_case)

    db.commit()

    return len(test_cases)

def get_test_case(
    db: Session,
    test_case_db_id: int
):

    return (
        db.query(TestCaseDB)
        .filter(
            TestCaseDB.id ==
            test_case_db_id
        )
        .first()
    )


def update_test_case_status(
    db: Session,
    test_case_db_id: int,
    review_status: str
):

    test_case = get_test_case(
        db,
        test_case_db_id
    )

    if test_case is None:
        return None

    test_case.review_status = (
        review_status
    )

    db.commit()

    db.refresh(test_case)

    return test_case

def get_scenario_test_cases(
    db: Session,
    scenario_db_id: int
):

    return (
        db.query(TestCaseDB)
        .filter(
            TestCaseDB.test_scenario_db_id
            == scenario_db_id
        )
        .order_by(
            TestCaseDB.id.asc()
        )
        .all()
    )

def save_ai_test_cases(
    db: Session,
    requirement_db_id: int,
    scenario_db_id: int,
    generated: AITestCaseGeneration
):

    test_case_ids = [
        test_case.test_case_id
        for test_case in generated.test_cases
    ]


    existing = (
        db.query(TestCaseDB)
        .filter(
            TestCaseDB.test_case_id.in_(
                test_case_ids
            )
        )
        .all()
    )


    if existing:

        existing_ids = [
            test_case.test_case_id
            for test_case in existing
        ]

        raise ValueError(
            "Test Case IDs already exist: "
            + ", ".join(existing_ids)
        )


    created_test_cases = []


    try:

        for generated_test_case in (
            generated.test_cases
        ):

            test_case = TestCaseDB(
                requirement_db_id=(
                    requirement_db_id
                ),

                test_scenario_db_id=(
                    scenario_db_id
                ),

                requirement_id=(
                    generated.requirement_id
                ),

                test_case_id=(
                    generated_test_case
                    .test_case_id
                ),

                title=(
                    generated_test_case
                    .title
                ),

                test_type=(
                    generated_test_case
                    .test_type
                ),

                priority=(
                    generated_test_case
                    .priority
                ),

                preconditions=(
                    generated_test_case
                    .preconditions
                ),

                test_data=(
                    generated_test_case
                    .test_data
                ),

                steps=[
                    step.model_dump()
                    for step
                    in generated_test_case.steps
                ],

                automation_candidate=(
                    generated_test_case
                    .automation_candidate
                ),

                review_status="draft"
            )


            db.add(
                test_case
            )


            created_test_cases.append(
                test_case
            )


        db.commit()


        for test_case in (
            created_test_cases
        ):

            db.refresh(
                test_case
            )


        return created_test_cases


    except Exception:

        db.rollback()

        raise
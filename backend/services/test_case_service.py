from sqlalchemy.orm import Session
from backend.agents.test_designer_agent import TestDesignerAgent
from backend.models.requirement import RequirementInput
from backend.models.test_case import (
    TestCase,
    TestCaseGenerationResponse,
)
from backend.db.test_scenario_model import (
    TestScenarioDB,
)
from backend.db.test_case_model import (
    TestCaseDB,
)


def generate_test_cases(
    requirement: RequirementInput
) -> TestCaseGenerationResponse:

    agent = TestDesignerAgent()

    ai_result = agent.generate(
        requirement
    )

    generated_test_cases = []

    for index, case in enumerate(
        ai_result.get("test_cases", []),
        start=1
    ):

        test_case = TestCase(
            test_case_id=(
                f"{requirement.requirement_id}-TC-{index:03d}"
            ),
            requirement_id=requirement.requirement_id,
            **case
        )

        generated_test_cases.append(
            test_case
        )

    return TestCaseGenerationResponse(
        requirement_id=requirement.requirement_id,
        total_test_cases=len(
            generated_test_cases
        ),
        test_cases=generated_test_cases
    )

def generate_test_cases_for_saved_requirement(
    db,
    saved_requirement
):

    requirement = RequirementInput(
        requirement_id=saved_requirement.requirement_id,
        title=saved_requirement.title,
        description=saved_requirement.description,
        application_type=(
            saved_requirement.application_type
        )
    )

    return generate_test_cases(
        requirement
    )

def get_test_scenario(
    db: Session,
    scenario_db_id: int
):

    return (
        db.query(TestScenarioDB)
        .filter(
            TestScenarioDB.id ==
            scenario_db_id
        )
        .first()
    )

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

def update_test_case_execution_type(
    db: Session,
    test_case: TestCaseDB,
    execution_type: str
):

    if test_case is None:

        raise ValueError(
            "Test Case was not found"
        )


    review_status = str(
        test_case.review_status or ""
    ).strip().lower()


    if review_status != "approved":

        raise ValueError(
            "Test Case must be approved "
            "before execution type can "
            "be selected"
        )


    normalised = str(
        execution_type or ""
    ).strip().lower()


    allowed = {
        "manual",
        "automation",
        "both",
    }


    if normalised not in allowed:

        raise ValueError(
            "Execution type must be "
            "manual, automation or both"
        )


    test_case.execution_type = (
        normalised
    )


    try:

        db.commit()

        db.refresh(
            test_case
        )

        return test_case


    except Exception:

        db.rollback()

        raise
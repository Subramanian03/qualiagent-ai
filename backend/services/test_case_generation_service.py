from sqlalchemy.orm import Session

from backend.ai.errors import (
    AIProviderResponseError,
)

from backend.db.requirement_model import (
    RequirementDB,
)

from backend.db.test_scenario_model import (
    TestScenarioDB,
)

from backend.services.ai_requirement_analysis_service import (
    analyse_requirement_with_ai,
)

from backend.services.ai_test_case_generation_service import (
    generate_test_cases_with_ai,
)

from backend.services.test_case_persistence_service import (
    get_scenario_test_cases,
    save_ai_test_cases,
)


def generate_and_save_ai_test_cases(
    db: Session,
    requirement: RequirementDB,
    scenario: TestScenarioDB
):

    if (
        scenario.requirement_db_id !=
        requirement.id
    ):
        raise ValueError(
            "Scenario does not belong "
            "to this Requirement"
        )


    existing = get_scenario_test_cases(
        db,
        scenario.id
    )


    if existing:

        raise ValueError(
            "Test Cases already exist "
            "for this Scenario"
        )


    analysis = (
        analyse_requirement_with_ai(
            requirement
        )
    )


    if not analysis.testable:

        raise AIProviderResponseError(
            "Requirement is not testable "
            "enough to generate Test Cases"
        )


    generated = (
        generate_test_cases_with_ai(
            requirement,
            scenario,
            analysis
        )
    )


    return save_ai_test_cases(
        db=db,
        requirement_db_id=(
            requirement.id
        ),
        scenario_db_id=(
            scenario.id
        ),
        generated=generated
    )
from sqlalchemy.orm import Session

from backend.ai.errors import (
    AIProviderResponseError,
)

from backend.db.requirement_model import (
    RequirementDB,
)

from backend.services.ai_requirement_analysis_service import (
    analyse_requirement_with_ai,
)

from backend.services.ai_scenario_generation_service import (
    generate_scenarios_with_ai,
)

from backend.services.test_scenario_service import (
    save_ai_scenarios,
)


def generate_and_save_ai_scenarios(
    db: Session,
    requirement: RequirementDB
):

    analysis = (
        analyse_requirement_with_ai(
            requirement
        )
    )


    if not analysis.testable:

        raise AIProviderResponseError(
            "Requirement is not testable "
            "enough to generate scenarios"
        )


    generated = (
        generate_scenarios_with_ai(
            requirement,
            analysis
        )
    )


    saved = save_ai_scenarios(
        db=db,
        requirement_db_id=(
            requirement.id
        ),
        generated=generated
    )


    return saved
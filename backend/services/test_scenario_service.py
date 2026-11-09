from sqlalchemy.orm import Session

from backend.db.requirement_model import (
    RequirementDB,
)
from backend.db.test_scenario_model import (
    TestScenarioDB,
)
from backend.models.test_scenario import (
    TestScenarioCreate,
)
from backend.models.ai_scenario_generation import (
    AIScenarioGeneration,
)


def get_requirement(
    db: Session,
    requirement_db_id: int
):

    return (
        db.query(RequirementDB)
        .filter(
            RequirementDB.id ==
            requirement_db_id
        )
        .first()
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


def get_requirement_test_scenarios(
    db: Session,
    requirement_db_id: int
):

    return (
        db.query(TestScenarioDB)
        .filter(
            TestScenarioDB.requirement_db_id
            == requirement_db_id
        )
        .order_by(
            TestScenarioDB.id.asc()
        )
        .all()
    )


def get_scenario_by_business_id(
    db: Session,
    requirement_db_id: int,
    scenario_id: str
):

    return (
        db.query(TestScenarioDB)
        .filter(
            TestScenarioDB.requirement_db_id
            == requirement_db_id,
            TestScenarioDB.scenario_id
            == scenario_id
        )
        .first()
    )


def create_test_scenario(
    db: Session,
    requirement_db_id: int,
    request: TestScenarioCreate
):

    scenario = TestScenarioDB(
        requirement_db_id=(
            requirement_db_id
        ),

        scenario_id=(
            request.scenario_id
        ),

        title=request.title,

        description=(
            request.description
        ),

        scenario_type=(
            request.scenario_type
        ),

        priority=(
            request.priority
        ),

        source=(
            request.source
        )
    )

    db.add(scenario)
    db.commit()
    db.refresh(scenario)

    return scenario

def save_ai_scenarios(
    db: Session,
    requirement_db_id: int,
    generated: AIScenarioGeneration
):

    scenario_ids = [
        scenario.scenario_id
        for scenario in generated.scenarios
    ]


    existing = (
        db.query(TestScenarioDB)
        .filter(
            TestScenarioDB.requirement_db_id
            == requirement_db_id,
            TestScenarioDB.scenario_id.in_(
                scenario_ids
            )
        )
        .all()
    )


    if existing:

        existing_ids = [
            scenario.scenario_id
            for scenario in existing
        ]

        raise ValueError(
            "Scenario IDs already exist "
            "for this requirement: "
            + ", ".join(existing_ids)
        )


    created_scenarios = []


    try:

        for generated_scenario in (
            generated.scenarios
        ):

            scenario = TestScenarioDB(
                requirement_db_id=(
                    requirement_db_id
                ),

                scenario_id=(
                    generated_scenario
                    .scenario_id
                ),

                title=(
                    generated_scenario
                    .title
                ),

                description=(
                    generated_scenario
                    .description
                ),

                scenario_type=(
                    generated_scenario
                    .scenario_type
                ),

                priority=(
                    generated_scenario
                    .priority
                ),

                source="ai"
            )

            db.add(scenario)

            created_scenarios.append(
                scenario
            )


        db.commit()


        for scenario in created_scenarios:

            db.refresh(
                scenario
            )


        return created_scenarios


    except Exception:

        db.rollback()

        raise
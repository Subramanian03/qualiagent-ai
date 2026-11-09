from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.db.database import get_db
from backend.models.automation import (
    AutomationScriptResponse,
)
from backend.services.automation_service import (
    AutomationReviewError,
    create_human_edited_automation_version,
    get_automation_for_test_case,
    get_ready_automation_for_test_case,
    get_automation_history_for_test_case,
    get_test_case,
    review_automation,
    save_real_generated_automation,
    create_ai_updated_automation_version,
)

from backend.db.automation_model import (
    AutomationScriptDB,
)

from backend.ai.errors import (
    AIProviderError,
)

from backend.db.project_model import (
    ProjectDB,
)

from backend.db.requirement_model import (
    RequirementDB,
)

from backend.db.test_case_model import (
    TestCaseDB,
)

from backend.db.test_scenario_model import (
    TestScenarioDB,
)

from backend.models.automation_input_schema import (
    AutomationInputSchema,
)

from backend.services.ai_automation_input_service import (
    analyse_automation_inputs_with_ai,
)

from backend.models.automation_runtime_input import (
    AutomationRuntimeInputSubmission,
)

from backend.services.automation_runtime_input_service import (
    get_persisted_input_schema,
    validate_runtime_inputs,
)

from backend.models.automation_review import (
    AutomationReviewRequest,
)

from backend.models.automation_edit import (
    AutomationHumanEditRequest,
)
from backend.models.automation_ai_update import (
    AutomationAIUpdateRequest,
)
from backend.automation_engines import (
    get_automation_engine,
)
from backend.automation_engines.errors import (
    AutomationEngineError,
)


router = APIRouter(
    prefix="/api/automation",
    tags=["Automation"]
)

def resolve_automation_context(
    db: Session,
    test_case_db_id: int
):

    test_case = (
        db.query(TestCaseDB)
        .filter(
            TestCaseDB.id ==
            test_case_db_id
        )
        .first()
    )

    if test_case is None:
        raise HTTPException(
            status_code=404,
            detail="Test Case not found"
        )


    if test_case.test_scenario_db_id is None:
        raise HTTPException(
            status_code=409,
            detail=(
                "Test Case is not linked "
                "to a Test Scenario"
            )
        )


    scenario = (
        db.query(TestScenarioDB)
        .filter(
            TestScenarioDB.id ==
            test_case.test_scenario_db_id
        )
        .first()
    )

    if scenario is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Parent Test Scenario "
                "not found"
            )
        )


    requirement = (
        db.query(RequirementDB)
        .filter(
            RequirementDB.id ==
            test_case.requirement_db_id
        )
        .first()
    )

    if requirement is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Parent Requirement "
                "not found"
            )
        )


    if (
        scenario.requirement_db_id !=
        requirement.id
    ):
        raise HTTPException(
            status_code=409,
            detail=(
                "Scenario and Test Case "
                "traceability is inconsistent"
            )
        )
    if (
    test_case.test_scenario_db_id !=
    scenario.id
):
        raise HTTPException(
           status_code=409,
           detail=(
            "Test Case and Scenario "
            "traceability is inconsistent"
        )
    )


    project = (
        db.query(ProjectDB)
        .filter(
            ProjectDB.id ==
            requirement.project_id
        )
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Parent Project not found"
        )


    return (
        project,
        requirement,
        scenario,
        test_case
    )

@router.post(
    "/test-case/{test_case_db_id}/generate-real",
    response_model=AutomationScriptResponse
)
def generate_real_test_case_automation(
    test_case_db_id: int,
    submission:
        AutomationRuntimeInputSubmission,
    db: Session = Depends(get_db)
):

    (
        project,
        requirement,
        scenario,
        test_case
    ) = resolve_automation_context(
        db,
        test_case_db_id
    )


    review_status = str(
        test_case.review_status or ""
    ).strip().lower()


    if review_status != "approved":

        raise HTTPException(
            status_code=409,
            detail=(
                "Test Case must be approved "
                "before automation generation"
            )
        )


    execution_type = str(
        test_case.execution_type or
        "manual"
    ).strip().lower()


    if execution_type not in {
        "automation",
        "both",
    }:

        raise HTTPException(
            status_code=409,
            detail=(
                "Test Case must be classified "
                "as AUTOMATION or BOTH before "
                "automation can be generated"
            )
        )


    try:

        # Re-derive the input schema on the
        # backend. Never trust a schema
        # submitted by the frontend.
        input_schema = (
            analyse_automation_inputs_with_ai(
                project,
                requirement,
                scenario,
                test_case
            )
        )


        runtime_inputs = (
            validate_runtime_inputs(
                input_schema,
                submission
            )
        )


        engine = (
            get_automation_engine(
                project
            )
        )


        generated = (
            engine.generate(
                project=project,
                requirement=requirement,
                scenario=scenario,
                test_case=test_case,
                input_schema=input_schema,
                runtime_inputs=runtime_inputs
            )
        )


        automation = (
    save_real_generated_automation(
        db=db,
        test_case_db_id=(
            test_case.id
        ),
        generated=generated,
        input_schema=(
            input_schema
        )
    )
)


        return automation

    except AutomationEngineError as exc:

        raise HTTPException(
            status_code=409,
            detail=str(exc)
        ) from exc

    except AIProviderError as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc)
        ) from exc


    except ValueError as exc:

        raise HTTPException(
            status_code=422,
            detail=str(exc)
        ) from exc

@router.post(
    "/test-case/{test_case_db_id}/inputs",
    response_model=AutomationInputSchema
)
def analyse_test_case_automation_inputs(
    test_case_db_id: int,
    db: Session = Depends(get_db)
):

    (
        project,
        requirement,
        scenario,
        test_case
    ) = resolve_automation_context(
        db,
        test_case_db_id
    )

    automation_engine = str(
        project.automation_engine or ""
    ).strip().lower()


    if automation_engine != "playwright":

        raise HTTPException(
            status_code=409,
            detail=(
                "Automation preparation for "
                f"'{automation_engine}' projects "
                "is not available yet. "
                "This QualiAgent build currently "
                "supports Playwright only."
            )
        )


    review_status = str(
        test_case.review_status or ""
    ).strip().lower()


    if review_status != "approved":

        raise HTTPException(
            status_code=409,
            detail=(
                "Test Case must be approved "
                "before automation preparation"
            )
        )


    execution_type = str(
        test_case.execution_type or
        "manual"
    ).strip().lower()


    if execution_type not in {
        "automation",
        "both",
    }:

        raise HTTPException(
            status_code=409,
            detail=(
                "Test Case must be classified "
                "as AUTOMATION or BOTH before "
                "automation can be prepared"
            )
        )


    try:

        return (
            analyse_automation_inputs_with_ai(
                project,
                requirement,
                scenario,
                test_case
            )
        )

    except AutomationEngineError as exc:

        raise HTTPException(
            status_code=409,
            detail=str(exc)
        ) from exc

    except AIProviderError as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc)
        ) from exc

@router.get(
    "/test-case/{test_case_db_id}/ready",
    response_model=AutomationScriptResponse
)
def get_ready_test_case_automation(
    test_case_db_id: int,
    db: Session = Depends(get_db)
):

    test_case = get_test_case(
        db,
        test_case_db_id
    )


    if test_case is None:

        raise HTTPException(
            status_code=404,
            detail="Test Case not found"
        )


    automation = (
        get_ready_automation_for_test_case(
            db,
            test_case_db_id
        )
    )


    if automation is None:

        raise HTTPException(
            status_code=404,
            detail=(
                "READY automation version "
                "not found for this Test Case"
            )
        )


    return automation


@router.get(
    "/test-case/{test_case_db_id}/execution-inputs",
    response_model=AutomationInputSchema
)
def get_test_case_execution_inputs(
    test_case_db_id: int,
    db: Session = Depends(get_db)
):

    test_case = get_test_case(
        db,
        test_case_db_id
    )


    if test_case is None:

        raise HTTPException(
            status_code=404,
            detail="Test Case not found"
        )


    automation = (
        get_ready_automation_for_test_case(
            db,
            test_case_db_id
        )
    )


    if automation is None:

        raise HTTPException(
            status_code=409,
            detail=(
                "READY automation version "
                "not found for this Test Case"
            )
        )


    try:

        return (
            get_persisted_input_schema(
                automation
            )
        )


    except ValueError as exc:

        raise HTTPException(
            status_code=409,
            detail=str(exc)
        ) from exc

def get_test_case_execution_inputs(
    test_case_db_id: int,
    db: Session = Depends(get_db)
):

    test_case = get_test_case(
        db,
        test_case_db_id
    )


    if test_case is None:

        raise HTTPException(
            status_code=404,
            detail="Test Case not found"
        )


    automation = (
        get_ready_automation_for_test_case(
            db,
            test_case_db_id
        )
    )


    if automation is None:

        raise HTTPException(
            status_code=409,
            detail=(
                "READY automation version "
                "not found for this Test Case"
            )
        )


    try:

        return (
            get_persisted_input_schema(
                automation
            )
        )


    except ValueError as exc:

        raise HTTPException(
            status_code=409,
            detail=str(exc)
        ) from exc
@router.get(
    "/test-case/{test_case_db_id}/history",
    response_model=list[
        AutomationScriptResponse
    ]
)
def get_test_case_automation_history(
    test_case_db_id: int,
    db: Session = Depends(get_db)
):

    test_case = get_test_case(
        db,
        test_case_db_id
    )


    if test_case is None:

        raise HTTPException(
            status_code=404,
            detail="Test Case not found"
        )


    return (
        get_automation_history_for_test_case(
            db,
            test_case_db_id
        )
    )

@router.get(
    "/test-case/{test_case_db_id}",
    response_model=AutomationScriptResponse
)
def get_test_case_automation(
    test_case_db_id: int,
    db: Session = Depends(get_db)
):

    test_case = get_test_case(
        db,
        test_case_db_id
    )

    if test_case is None:
        raise HTTPException(
            status_code=404,
            detail="Test case not found"
        )

    automation = get_automation_for_test_case(
        db,
        test_case_db_id
    )

    if automation is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Automation not found "
                "for this test case"
            )
        )

    return automation


@router.post(
    "/{automation_id}/edit",
    response_model=AutomationScriptResponse,
    status_code=201
)
def create_human_edited_automation(
    automation_id: int,
    request: AutomationHumanEditRequest,
    db: Session = Depends(get_db)
):

    source_automation = (
        db.query(
            AutomationScriptDB
        )
        .filter(
            AutomationScriptDB.id ==
            automation_id
        )
        .first()
    )


    if source_automation is None:

        raise HTTPException(
            status_code=404,
            detail=(
                "Source automation "
                "version not found"
            )
        )


    (
        project,
        requirement,
        scenario,
        test_case
    ) = resolve_automation_context(
        db,
        source_automation.test_case_db_id
    )


    try:

        engine = (
            get_automation_engine(
                project
            )
        )


        source_engine = str(
            source_automation.engine or
            source_automation.framework or
            ""
        ).strip().lower()


        source_language = str(
            source_automation.language or ""
        ).strip().lower()


        if (
            source_engine !=
            engine.engine_name
        ):

            raise AutomationReviewError(
                "Source automation engine "
                "does not match the current "
                "Project automation engine"
            )


        if (
            source_language !=
            engine.language
        ):

            raise AutomationReviewError(
                "Source automation language "
                "does not match the current "
                "Project automation language"
            )


        engine.validate_source(
            request.code
        )


        return (
            create_human_edited_automation_version(
                db=db,
                source_automation=(
                    source_automation
                ),
                request=request
            )
        )


    except AutomationEngineError as exc:

        raise HTTPException(
            status_code=409,
            detail=str(exc)
        ) from exc


    except AutomationReviewError as exc:

        raise HTTPException(
            status_code=409,
            detail=str(exc)
        ) from exc
    
@router.post(
    "/{automation_id}/ai-update",
    response_model=AutomationScriptResponse,
    status_code=201
)
def create_ai_updated_automation(
    automation_id: int,
    request: AutomationAIUpdateRequest,
    db: Session = Depends(get_db)
):

    source_automation = (
        db.query(
            AutomationScriptDB
        )
        .filter(
            AutomationScriptDB.id ==
            automation_id
        )
        .first()
    )


    if source_automation is None:

        raise HTTPException(
            status_code=404,
            detail=(
                "Source automation "
                "version not found"
            )
        )


    try:

        (
            project,
            requirement,
            scenario,
            test_case
        ) = resolve_automation_context(
            db,
            source_automation
            .test_case_db_id
        )

        review_status = str(
            test_case.review_status or ""
        ).strip().lower()


        if review_status != "approved":

            raise AutomationReviewError(
                "Parent Test Case must remain "
                "approved before AI update"
            )


        execution_type = str(
            test_case.execution_type or
            "manual"
        ).strip().lower()


        if execution_type not in {
            "automation",
            "both",
        }:

            raise AutomationReviewError(
                "Parent Test Case must be "
                "classified as AUTOMATION "
                "or BOTH before AI update"
            )


        engine = (
            get_automation_engine(
                project
            )
        )


        generated = (
            engine.update_with_ai(
                automation=source_automation,
                project=project,
                requirement=requirement,
                scenario=scenario,
                test_case=test_case,
                request=request
            )
        )


        return (
            create_ai_updated_automation_version(
                db=db,
                source_automation=(
                    source_automation
                ),
                generated=generated,
                request=request
            )
        )

    except AutomationEngineError as exc:

        raise HTTPException(
            status_code=409,
            detail=str(exc)
        ) from exc

    except AutomationReviewError as exc:

        raise HTTPException(
            status_code=409,
            detail=str(exc)
        ) from exc


    except AIProviderError as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc)
        ) from exc


    except ValueError as exc:

        raise HTTPException(
            status_code=422,
            detail=str(exc)
        ) from exc
    
@router.patch(
    "/{automation_id}/review",
    response_model=AutomationScriptResponse
)
def review_generated_automation(
    automation_id: int,
    request: AutomationReviewRequest,
    db: Session = Depends(get_db)
):

    automation = (
        db.query(
            AutomationScriptDB
        )
        .filter(
            AutomationScriptDB.id ==
            automation_id
        )
        .first()
    )


    if automation is None:

        raise HTTPException(
            status_code=404,
            detail="Automation not found"
        )


    (
        project,
        requirement,
        scenario,
        test_case
    ) = resolve_automation_context(
        db,
        automation.test_case_db_id
    )


    try:

        engine = (
            get_automation_engine(
                project
            )
        )


        automation_engine = str(
            automation.engine or
            automation.framework or
            ""
        ).strip().lower()


        automation_language = str(
            automation.language or ""
        ).strip().lower()


        if (
            automation_engine !=
            engine.engine_name
        ):

            raise AutomationReviewError(
                "Automation engine does not "
                "match the current Project "
                "automation engine"
            )


        if (
            automation_language !=
            engine.language
        ):

            raise AutomationReviewError(
                "Automation language does not "
                "match the current Project "
                "automation language"
            )


        engine.validate_source(
            automation.code
        )


        return review_automation(
            db=db,
            automation=automation,
            requested_status=(
                request.status
            )
        )


    except AutomationEngineError as exc:

        raise HTTPException(
            status_code=409,
            detail=str(exc)
        ) from exc


    except AutomationReviewError as exc:

        raise HTTPException(
            status_code=409,
            detail=str(exc)
        ) from exc
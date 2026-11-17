from copy import deepcopy

from sqlalchemy.orm import Session


from backend.db.automation_model import (
    AutomationScriptDB,
)

from backend.db.execution_model import (
    ExecutionDB,
)

from backend.models.failure_analysis import (
    CreateFailureSuggestionDraftRequest,
    CreateFailureSuggestionDraftResponse,
)

from backend.services.automation_service import (
    get_next_automation_version,
)

from backend.services.failure_analysis_policy import (
    ensure_execution_can_be_analysed,
)


class FailureSuggestionDraftError(
    ValueError
):
    pass


def clean_required_text(
    value,
    field_name: str
) -> str:

    cleaned = str(
        value or ""
    ).strip()


    if not cleaned:

        raise FailureSuggestionDraftError(
            f"{field_name} is required"
        )


    return cleaned


def create_failure_suggestion_draft(
    db: Session,
    *,
    execution_id: int,
    request: (
        CreateFailureSuggestionDraftRequest
    )
) -> CreateFailureSuggestionDraftResponse:

    if (
        request.source_execution_id !=
        execution_id
    ):

        raise FailureSuggestionDraftError(
            (
                "Source Execution ID does not "
                "match the requested Execution."
            )
        )


    execution = (
        db.query(
            ExecutionDB
        )
        .filter(
            ExecutionDB.id ==
            execution_id
        )
        .first()
    )


    if execution is None:

        raise FailureSuggestionDraftError(
            "Execution not found"
        )


    ensure_execution_can_be_analysed(
        execution
    )


    frozen_automation_id = (
        execution.automation_script_id
    )


    if frozen_automation_id is None:

        raise FailureSuggestionDraftError(
            (
                "The failed Execution is not "
                "linked to an Automation version."
            )
        )


    if (
        request.parent_automation_version_id !=
        frozen_automation_id
    ):

        raise FailureSuggestionDraftError(
            (
                "The selected parent Automation "
                "is not the frozen Automation "
                "used by this Execution."
            )
        )


    parent_automation = (
        db.query(
            AutomationScriptDB
        )
        .filter(
            AutomationScriptDB.id ==
            frozen_automation_id
        )
        .first()
    )


    if parent_automation is None:

        raise FailureSuggestionDraftError(
            "Parent Automation version not found"
        )


    if not (
        parent_automation.code
        and
        parent_automation.code.strip()
    ):

        raise FailureSuggestionDraftError(
            (
                "Parent Automation version "
                "does not contain code."
            )
        )


    if not parent_automation.input_schema:

        raise FailureSuggestionDraftError(
            (
                "Parent Automation version "
                "does not contain a persisted "
                "input schema."
            )
        )


    submitted_code = (
        clean_required_text(
            request.code,
            "Automation code"
        )
    )


    rationale = (
        clean_required_text(
            request.rationale,
            "Suggestion rationale"
        )
    )


    if (
        submitted_code ==
        parent_automation.code.strip()
    ):

        raise FailureSuggestionDraftError(
            (
                "The submitted Automation code "
                "is unchanged from the frozen "
                "parent version."
            )
        )


    source_status = str(
        parent_automation.status or ""
    ).strip().lower()


    if source_status not in {
        "ready",
        "draft",
        "rejected",
        "superseded",
    }:

        raise FailureSuggestionDraftError(
            (
                "Parent Automation version "
                "has an invalid status."
            )
        )


    next_version = (
        get_next_automation_version(
            db,
            parent_automation.test_case_db_id
        )
    )


    change_summary = (
        "AI failure suggestion reviewed by "
        "a human. "
        f"Execution #{execution.id}; "
        f"classification="
        f"{request.classification}; "
        f"recommendation="
        f"{request.recommendation_type}. "
        f"Rationale: {rationale}"
    )


    new_automation = (
        AutomationScriptDB(
            test_case_db_id=(
                parent_automation
                .test_case_db_id
            ),

            framework=(
                parent_automation.framework
            ),

            engine=(
                parent_automation.engine
                or
                parent_automation.framework
            ),

            language=(
                parent_automation.language
            ),

            code=(
                submitted_code
            ),

            status="draft",

            version=(
                next_version
            ),

            input_schema=(
                deepcopy(
                    parent_automation.input_schema
                )
            ),

            source=(
                "ai_failure_suggestion"
            ),

            change_summary=(
                change_summary
            ),

            parent_version_id=(
                parent_automation.id
            ),

            source_execution_id=(
    execution.id
),

            created_by=None,

            reviewed_by=None,

            reviewed_at=None,
        )
    )


    try:

        db.add(
            new_automation
        )


        db.commit()


        db.refresh(
            new_automation
        )


    except Exception:

        db.rollback()

        raise


    return (
        CreateFailureSuggestionDraftResponse(
            source_execution_id=(
                execution.id
            ),

            parent_automation_version_id=(
                parent_automation.id
            ),

            test_case_db_id=(
    parent_automation.test_case_db_id
),

            created_automation_version_id=(
                new_automation.id
            ),

            created_version_number=(
                new_automation.version
            ),

            status=(
                new_automation.status
            ),

            human_review_required=True,

            source_execution_changed=False,

            parent_automation_changed=False
        )
    )
from fastapi import APIRouter

from backend.ai.factory import get_ai_provider
from backend.ai.prompts import REQUIREMENT_ANALYST_SYSTEM_PROMPT
from backend.agents.requirement_agent import RequirementAnalystAgent
from backend.models.requirement import RequirementInput


router = APIRouter(
    prefix="/api/ai",
    tags=["AI"],
)


@router.get("/test")
def test_ai_provider():

    provider = get_ai_provider()

    result = provider.generate(
        system_prompt=REQUIREMENT_ANALYST_SYSTEM_PROMPT,
        user_prompt=(
            "Analyse a requirement for customer login."
        ),
    )

    return {
        "status": "success",
        "ai_result": result,
    }

@router.post("/analyse-requirement")
def analyse_requirement_with_ai(
    requirement: RequirementInput
):

    agent = RequirementAnalystAgent()

    result = agent.analyse(
        requirement
    )

    return {
        "status": "success",
        "analysis": result,
    }
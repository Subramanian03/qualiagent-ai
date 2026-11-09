from backend.ai.factory import get_ai_provider
from backend.ai.prompts import REQUIREMENT_ANALYST_SYSTEM_PROMPT
from backend.models.requirement import (
    AIRequirementAnalysis,
    RequirementInput,
)


class RequirementAnalystAgent:

    def __init__(self):
        self.provider = get_ai_provider()

    def build_user_prompt(
        self,
        requirement: RequirementInput
    ) -> str:

        return f"""
Analyse the following software requirement.

Requirement ID:
{requirement.requirement_id}

Title:
{requirement.title}

Application Type:
{requirement.application_type}

Requirement:
{requirement.description}

Perform a QA-focused requirement analysis.

Identify:
- acceptance criteria
- positive scenarios
- negative scenarios
- boundary scenarios
- security considerations
- usability considerations
- ambiguities
- missing information
- recommended testing types
"""

    def analyse(
        self,
        requirement: RequirementInput
    ):

        user_prompt = self.build_user_prompt(
            requirement
        )

        return self.provider.generate(
            system_prompt=(
                REQUIREMENT_ANALYST_SYSTEM_PROMPT
            ),
            user_prompt=user_prompt,
            task="requirement_analysis",
        )
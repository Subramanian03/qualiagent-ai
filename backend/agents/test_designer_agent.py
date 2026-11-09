from backend.ai.factory import get_ai_provider
from backend.ai.prompts import TEST_DESIGNER_SYSTEM_PROMPT
from backend.models.requirement import RequirementInput


class TestDesignerAgent:

    def __init__(self):
        self.provider = get_ai_provider()

    def build_user_prompt(
        self,
        requirement: RequirementInput
    ) -> str:

        return f"""
Generate QA test cases for this requirement.

Requirement ID:
{requirement.requirement_id}

Title:
{requirement.title}

Application Type:
{requirement.application_type}

Description:
{requirement.description}
"""

    def generate(
        self,
        requirement: RequirementInput
    ):

        user_prompt = self.build_user_prompt(
            requirement
        )

        return self.provider.generate(
            system_prompt=TEST_DESIGNER_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            task="test_case_generation"
        )
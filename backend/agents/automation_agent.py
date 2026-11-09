from backend.ai.factory import (
    get_ai_provider,
)
from backend.ai.prompts import (
    AUTOMATION_GENERATOR_SYSTEM_PROMPT,
)
from backend.models.test_case import TestCase


class AutomationAgent:

    def __init__(self):
        self.provider = get_ai_provider()


    def build_user_prompt(
        self,
        test_case: TestCase
    ) -> str:

        steps = "\n".join(
            (
                f"{step.step_number}. "
                f"{step.action} | "
                f"Expected: "
                f"{step.expected_result}"
            )
            for step in test_case.steps
        )

        preconditions = "\n".join(
            test_case.preconditions
        )

        test_data = "\n".join(
            test_case.test_data
        )

        return f"""
Generate Playwright JavaScript automation.

Test Case ID:
{test_case.test_case_id}

Title:
{test_case.title}

Type:
{test_case.test_type}

Priority:
{test_case.priority}

Preconditions:
{preconditions}

Test Data:
{test_data}

Steps:
{steps}
"""


    def generate(
        self,
        test_case: TestCase
    ):

        user_prompt = self.build_user_prompt(
            test_case
        )

        return self.provider.generate(
            system_prompt=(
                AUTOMATION_GENERATOR_SYSTEM_PROMPT
            ),
            user_prompt=user_prompt,
            task="automation_generation"
        )
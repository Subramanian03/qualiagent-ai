from backend.automation_engines.base import (
    AutomationEngine,
)

from backend.automation_engines.errors import (
    AutomationEngineNotSupportedError,
)


class SeleniumPythonEngine(
    AutomationEngine
):

    engine_name = "selenium"

    language = "python"


    def generate(
        self,
        *,
        project,
        requirement,
        scenario,
        test_case,
        input_schema,
        runtime_inputs
    ):

        raise AutomationEngineNotSupportedError(
            "Selenium automation generation "
            "is not implemented yet"
        )


    def update_with_ai(
        self,
        *,
        automation,
        project,
        requirement,
        scenario,
        test_case,
        request
    ):

        raise AutomationEngineNotSupportedError(
            "Selenium AI automation update "
            "is not implemented yet"
        )


    def validate_source(
        self,
        source_code: str
    ) -> None:

        raise AutomationEngineNotSupportedError(
            "Selenium source validation "
            "is not implemented yet"
        )

    def execute(
        self,
        *,
        automation,
        execution,
        runtime_inputs
    ):

        raise AutomationEngineNotSupportedError(
            "Selenium automation execution "
            "is not implemented yet"
        )
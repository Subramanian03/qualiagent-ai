from backend.automation_engines.base import (
    AutomationEngine,
)

from backend.automation_engines.errors import (
    AutomationEngineConfigurationError,
)

from backend.services.ai_automation_update_service import (
    update_automation_with_ai,
)

from backend.services.ai_playwright_generation_service import (
    generate_playwright_with_ai,
)

from backend.services.playwright_runner_service import (
    run_playwright,
)


class PlaywrightJavaScriptEngine(
    AutomationEngine
):

    engine_name = "playwright"

    language = "javascript"


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

        self.validate_project(
            project
        )


        generated = (
            generate_playwright_with_ai(
                project,
                requirement,
                scenario,
                test_case,
                input_schema,
                runtime_inputs
            )
        )


        self.validate_source(
            generated.code
        )


        return generated


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

        self.validate_project(
            project
        )


        generated = (
            update_automation_with_ai(
                automation=automation,
                test_case=test_case,
                requirement=requirement,
                scenario=scenario,
                project=project,
                request=request
            )
        )


        self.validate_source(
            generated.code
        )


        return generated


    def validate_project(
        self,
        project
    ) -> None:

        project_engine = str(
            getattr(
                project,
                "automation_engine",
                ""
            )
            or ""
        ).strip().lower()


        project_language = str(
            getattr(
                project,
                "automation_language",
                ""
            )
            or ""
        ).strip().lower()


        if (
            project_engine !=
            self.engine_name
        ):

            raise (
                AutomationEngineConfigurationError(
                    "Project automation engine "
                    "does not match the "
                    "Playwright provider"
                )
            )


        if (
            project_language !=
            self.language
        ):

            raise (
                AutomationEngineConfigurationError(
                    "Playwright currently "
                    "requires JavaScript"
                )
            )


    def validate_source(
        self,
        source_code: str
    ) -> None:

        cleaned = str(
            source_code or ""
        ).strip()


        if not cleaned:

            raise (
                AutomationEngineConfigurationError(
                    "Playwright source code "
                    "is required"
                )
            )


        required_markers = [
            "@playwright/test",
            "test(",
        ]


        for marker in required_markers:

            if marker not in cleaned:

                raise (
                    AutomationEngineConfigurationError(
                        "Playwright source is "
                        "missing required marker: "
                        f"{marker}"
                    )
                )


    def execute(
        self,
        *,
        automation,
        execution,
        runtime_inputs
    ):

        self.validate_source(
            automation.code
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
            self.engine_name
        ):

            raise (
                AutomationEngineConfigurationError(
                    "Automation engine does not "
                    "match the Playwright provider"
                )
            )


        if (
            automation_language !=
            self.language
        ):

            raise (
                AutomationEngineConfigurationError(
                    "Playwright execution requires "
                    "JavaScript automation"
                )
            )


        return run_playwright(
            execution_id=execution.id,
            automation_code=automation.code,
            runtime_environment=runtime_inputs
        )
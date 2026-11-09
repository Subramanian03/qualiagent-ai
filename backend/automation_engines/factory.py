from backend.automation_engines.errors import (
    AutomationEngineConfigurationError,
    AutomationEngineNotSupportedError,
)

from backend.automation_engines.playwright_engine import (
    PlaywrightJavaScriptEngine,
)

from backend.automation_engines.selenium_engine import (
    SeleniumPythonEngine,
)


def get_automation_engine(
    project
):

    engine_name = str(
        getattr(
            project,
            "automation_engine",
            ""
        )
        or ""
    ).strip().lower()


    language = str(
        getattr(
            project,
            "automation_language",
            ""
        )
        or ""
    ).strip().lower()


    if not engine_name:

        raise (
            AutomationEngineConfigurationError(
                "Project automation engine "
                "is not configured"
            )
        )


    if (
        engine_name == "playwright"
        and
        language == "javascript"
    ):

        return (
            PlaywrightJavaScriptEngine()
        )


    if (
        engine_name == "selenium"
        and
        language == "python"
    ):

        return (
            SeleniumPythonEngine()
        )


    if engine_name not in {
        "playwright",
        "selenium",
    }:

        raise (
            AutomationEngineNotSupportedError(
                "Unsupported automation "
                f"engine: {engine_name}"
            )
        )


    raise (
        AutomationEngineConfigurationError(
            "Unsupported engine-language "
            "combination: "
            f"{engine_name} + {language}"
        )
    )
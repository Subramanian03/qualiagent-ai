class AutomationEngineError(
    ValueError
):
    pass


class AutomationEngineNotSupportedError(
    AutomationEngineError
):
    pass


class AutomationEngineConfigurationError(
    AutomationEngineError
):
    pass
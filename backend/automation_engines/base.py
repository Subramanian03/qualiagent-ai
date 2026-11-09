from abc import ABC
from abc import abstractmethod


class AutomationEngine(
    ABC
):

    engine_name: str
    language: str


    @abstractmethod
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
        """
        Generate automation source code for
        an approved Test Case.
        """
        raise NotImplementedError


    @abstractmethod
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
        """
        Generate an updated automation
        version from existing source code.
        """
        raise NotImplementedError


    @abstractmethod
    def validate_source(
        self,
        source_code: str
    ) -> None:
        """
        Validate source code before it can
        become a reviewable automation
        version.
        """
        raise NotImplementedError

    @abstractmethod
    def execute(
        self,
        *,
        automation,
        execution,
        runtime_inputs
    ):
        """
        Execute one frozen automation
        version and return the runner result.

        The caller remains responsible for
        persisting the final execution
        status and evidence metadata.
        """
        raise NotImplementedError
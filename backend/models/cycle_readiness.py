from pydantic import BaseModel
from pydantic import ConfigDict

from typing import Literal


class ReadyAutomationSummary(
    BaseModel
):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int

    version: int

    engine: str

    language: str

    status: Literal[
        "ready"
    ]


class CycleReadyTestCase(
    BaseModel
):

    id: int

    test_case_id: str

    title: str

    test_type: str

    priority: str

    automation_candidate: bool

    execution_type: Literal[
        "manual",
        "automation",
        "both"
    ]

    manual_eligible: bool

    automation_eligible: bool

    ready_automation: (
        ReadyAutomationSummary |
        None
    ) = None


class CycleReadyScenario(
    BaseModel
):

    id: int

    scenario_id: str

    title: str

    test_cases: list[
        CycleReadyTestCase
    ]


class CycleReadyRequirement(
    BaseModel
):

    id: int

    requirement_id: str

    title: str

    scenarios: list[
        CycleReadyScenario
    ]


class ProjectCycleReadiness(
    BaseModel
):

    project_id: int

    project_name: str

    requirements: list[
        CycleReadyRequirement
    ]
from typing import Literal

from pydantic import BaseModel, Field

from datetime import datetime

from pydantic import ConfigDict


class RequirementInput(BaseModel):
    requirement_id: str = Field(
        min_length=1,
        max_length=50,
        examples=["REQ-001"]
    )

    title: str = Field(
        min_length=3,
        max_length=200,
        examples=["User Login"]
    )

    description: str = Field(
        min_length=10,
        max_length=5000,
        examples=[
            "A registered user should be able to log in "
            "using a valid email address and password."
        ]
    )

    application_type: Literal["web", "mobile", "api"]


class RequirementAnalysisResponse(BaseModel):
    requirement_id: str
    summary: str
    application_type: str
    testable: bool
    risk_level: Literal["low", "medium", "high"]
    identified_keywords: list[str]
    suggested_test_types: list[str]
    acceptance_criteria: list[str]
    questions: list[str]
    message: str


class AIRequirementAnalysis(BaseModel):
    requirement_id: str
    requirement_summary: str

    clarity_score: int = Field(
        ge=1,
        le=10
    )

    testable: bool

    risk_level: Literal[
        "low",
        "medium",
        "high"
    ]

    acceptance_criteria: list[str]

    positive_scenarios: list[str]

    negative_scenarios: list[str]

    boundary_scenarios: list[str]

    security_considerations: list[str]

    usability_considerations: list[str]

    ambiguities: list[str]

    missing_information: list[str]

    recommended_test_types: list[str]


class RequirementCreate(BaseModel):

    requirement_id: str = Field(
        min_length=1,
        max_length=50
    )

    title: str = Field(
        min_length=3,
        max_length=200
    )

    description: str = Field(
        min_length=10,
        max_length=5000
    )

    application_type: Literal[
        "web",
        "mobile",
        "api"
    ]


class RequirementResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    requirement_id: str
    project_id: int
    title: str
    description: str
    application_type: str
    created_at: datetime
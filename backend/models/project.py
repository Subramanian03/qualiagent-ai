from datetime import datetime
from typing import Literal
from pydantic import field_validator
from pydantic import model_validator

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class ProjectCreate(BaseModel):

    name: str = Field(
        min_length=3,
        max_length=200
    )

    description: str = Field(
        min_length=5,
        max_length=1000
    )

    application_type: Literal[
        "web",
        "mobile",
        "api"
    ]

    automation_engine: str = (
        "playwright"
    )

    automation_language: str = (
        "javascript"
    )

    default_browser: str = (
        "chromium"
    )

    @field_validator(
        "application_type"
    )
    @classmethod
    def validate_application_type(
        cls,
        value: str
    ):

        normalised = (
            value.strip().lower()
        )

        if normalised != "web":

            raise ValueError(
                "QualiAgent currently "
                "supports Web projects only"
            )

        return normalised

    @field_validator(
        "automation_engine"
    )
    @classmethod
    def validate_automation_engine(
        cls,
        value: str
    ):

        normalised = (
            value.strip().lower()
        )

        allowed = {
            "playwright",
            "selenium",
        }


        if normalised not in allowed:

            raise ValueError(
                "automation_engine must be "
                "playwright or selenium"
            )


        return normalised

    @field_validator(
        "automation_language"
    )
    @classmethod
    def validate_automation_language(
        cls,
        value: str
    ):

        normalised = (
            value.strip().lower()
        )


        if normalised not in {
            "javascript",
            "python",
        }:

            raise ValueError(
                "automation_language must "
                "be javascript or python"
            )


        return normalised

    @field_validator(
        "default_browser"
    )
    @classmethod
    def validate_default_browser(
        cls,
        value: str
    ):

        normalised = (
            value.strip().lower()
        )


        if normalised not in {
            "chromium",
            "firefox",
            "webkit",
        }:

            raise ValueError(
                "default_browser must be "
                "chromium, firefox or webkit"
            )


        return normalised

    @model_validator(
        mode="after"
    )
    def validate_engine_language(
        self
    ):

        if (
            self.automation_engine ==
            "playwright"
            and
            self.automation_language !=
            "javascript"
        ):

            raise ValueError(
                "Playwright currently requires "
                "JavaScript in QualiAgent"
            )


        if (
            self.automation_engine ==
            "selenium"
            and
            self.automation_language !=
            "python"
        ):

            raise ValueError(
                "Selenium currently requires "
                "Python in QualiAgent"
            )


        return self

class ProjectResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    name: str
    description: str
    application_type: str
    automation_engine: str
    automation_language: str
    default_browser: str
    created_at: datetime
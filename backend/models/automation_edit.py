from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import field_validator


class AutomationHumanEditRequest(
    BaseModel
):

    model_config = ConfigDict(
        extra="forbid"
    )


    code: str = Field(
        min_length=20,
        max_length=100000
    )


    change_summary: str = Field(
        min_length=3,
        max_length=500
    )


    @field_validator(
        "code",
        "change_summary",
        mode="before"
    )
    @classmethod
    def clean_text(
        cls,
        value
    ):

        if isinstance(
            value,
            str
        ):
            return value.strip()

        return value
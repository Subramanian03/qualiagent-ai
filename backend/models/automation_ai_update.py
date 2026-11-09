from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import field_validator


class AutomationAIUpdateRequest(
    BaseModel
):

    model_config = ConfigDict(
        extra="forbid"
    )


    instruction: str = Field(
        min_length=5,
        max_length=2000
    )


    @field_validator(
        "instruction",
        mode="before"
    )
    @classmethod
    def clean_instruction(
        cls,
        value
    ):

        if isinstance(
            value,
            str
        ):
            return value.strip()

        return value
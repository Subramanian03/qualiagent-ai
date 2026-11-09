from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import HttpUrl


class ExecutionConfigUpsert(BaseModel):

    environment_name: str = Field(
        default="QA",
        min_length=1,
        max_length=100
    )

    base_url: HttpUrl

    test_username: str | None = Field(
        default=None,
        max_length=255
    )

    test_first_name: str | None = Field(
        default=None,
        max_length=255
    )

    test_last_name: str | None = Field(
        default=None,
        max_length=255
    )

    test_postal_code: str | None = Field(
        default=None,
        max_length=50
    )

    credentials_required: bool = False


class ExecutionConfigResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    project_id: int

    environment_name: str
    base_url: str

    test_username: str | None
    test_first_name: str | None
    test_last_name: str | None
    test_postal_code: str | None

    credentials_required: bool

    created_at: datetime
    updated_at: datetime
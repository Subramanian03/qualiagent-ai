from datetime import datetime
from typing import Literal

from pydantic import BaseModel
from pydantic import ConfigDict


class AutomationScriptCreate(BaseModel):

    framework: Literal[
        "playwright"
    ] = "playwright"

    language: Literal[
        "javascript"
    ] = "javascript"


class AutomationScriptResponse(
    BaseModel
):

    id: int

    test_case_db_id: int

    framework: str

    language: str

    code: str

    status: str

    version: int = 1

    engine: str | None = None

    input_schema: dict | None = None

    source: str | None = None

    parent_version_id: int | None = None

    change_summary: str | None = None


    model_config = {
        "from_attributes": True
    }
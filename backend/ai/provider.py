from abc import ABC
from abc import abstractmethod
from typing import Any


class AIProvider(ABC):

    @abstractmethod
    def generate(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        task: str
    ) -> dict[str, Any]:
        """
Generate one structured JSON object for
a supported QualiAgent AI task.

Task-specific Pydantic validation occurs
in the calling agent/service.
"""

        raise NotImplementedError
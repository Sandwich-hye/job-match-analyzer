from typing import Protocol


class LLMClient(Protocol):
    def generate(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        response_schema: dict[str, object] | None = None,
    ) -> str:
        ...
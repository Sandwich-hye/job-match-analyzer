from groq import Groq

from app.settings import GroqSettings


class GroqLLMClient:
    def __init__(
        self,
        settings: GroqSettings,
        sdk_client: Groq | None = None,
    ) -> None:
        self._settings = settings
        self._client = (
            sdk_client
            if sdk_client is not None
            else Groq(api_key=settings.api_key)
        )

    def generate(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        response_schema: (
            dict[str, object] | None
        ) = None,
    ) -> str:
        messages = [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ]

        if response_schema is None:
            completion = (
                self._client.chat.completions.create(
                    model=self._settings.model,
                    messages=messages,
                    temperature=0,
                )
            )
        else:
            completion = (
                self._client.chat.completions.create(
                    model=self._settings.model,
                    messages=messages,
                    temperature=0,
                    response_format={
                        "type": "json_schema",
                        "json_schema": {
                            "name": "job_extraction",
                            "strict": False,
                            "schema": response_schema,
                        },
                    },
                )
            )

        if not completion.choices:
            raise ValueError(
                "Groq returned no completion choices"
            )

        content = (
            completion
            .choices[0]
            .message
            .content
        )

        if content is None or not content.strip():
            raise ValueError(
                "Groq returned empty content"
            )

        return content.strip()
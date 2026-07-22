from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from app.groq_client import GroqLLMClient
from app.settings import GroqSettings


def create_completion(
    content: str | None,
) -> SimpleNamespace:
    return SimpleNamespace(
        choices=[
            SimpleNamespace(
                message=SimpleNamespace(
                    content=content,
                )
            )
        ]
    )


def test_groq_client_returns_generated_content(
) -> None:
    sdk_client = Mock()

    sdk_client.chat.completions.create.return_value = (
        create_completion(
            '{"job_title": "Software Engineer"}'
        )
    )

    settings = GroqSettings(
        api_key="test-api-key",
        model="openai/gpt-oss-20b",
    )

    client = GroqLLMClient(
        settings=settings,
        sdk_client=sdk_client,
    )

    result = client.generate(
        system_prompt="System instructions",
        user_prompt="Extract this job.",
        response_schema={
            "type": "object",
            "properties": {},
        },
    )

    assert result == (
        '{"job_title": "Software Engineer"}'
    )


def test_groq_client_sends_expected_request(
) -> None:
    sdk_client = Mock()

    sdk_client.chat.completions.create.return_value = (
        create_completion("{}")
    )

    settings = GroqSettings(
        api_key="test-api-key",
        model="openai/gpt-oss-20b",
    )

    client = GroqLLMClient(
        settings=settings,
        sdk_client=sdk_client,
    )

    schema = {
        "type": "object",
        "properties": {},
    }

    client.generate(
        system_prompt="System instructions",
        user_prompt="Extract this job.",
        response_schema=schema,
    )

    request = (
        sdk_client
        .chat
        .completions
        .create
        .call_args
        .kwargs
    )

    assert request["model"] == (
        "openai/gpt-oss-20b"
    )

    assert request["messages"] == [
        {
            "role": "system",
            "content": "System instructions",
        },
        {
            "role": "user",
            "content": "Extract this job.",
        },
    ]

    assert request["response_format"] == {
        "type": "json_schema",
        "json_schema": {
            "name": "job_extraction",
            "strict": False,
            "schema": schema,
        },
    }


def test_groq_client_rejects_empty_content(
) -> None:
    sdk_client = Mock()

    sdk_client.chat.completions.create.return_value = (
        create_completion(None)
    )

    settings = GroqSettings(
        api_key="test-api-key",
        model="openai/gpt-oss-20b",
    )

    client = GroqLLMClient(
        settings=settings,
        sdk_client=sdk_client,
    )

    with pytest.raises(
        ValueError,
        match="Groq returned empty content",
    ):
        client.generate(
            system_prompt="System instructions",
            user_prompt="Extract this job.",
        )
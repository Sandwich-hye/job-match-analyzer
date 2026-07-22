import pytest

from app.settings import (
    GroqSettings,
    load_groq_settings,
)


def test_load_groq_settings_reads_environment_variables(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(
        "GROQ_API_KEY",
        "test-api-key",
    )
    monkeypatch.setenv(
        "GROQ_MODEL",
        "test-model",
    )

    result = load_groq_settings(
        env_file=None,
    )

    assert isinstance(result, GroqSettings)
    assert result.api_key == "test-api-key"
    assert result.model == "test-model"


def test_load_groq_settings_strips_whitespace(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(
        "GROQ_API_KEY",
        "  test-api-key  ",
    )
    monkeypatch.setenv(
        "GROQ_MODEL",
        "  test-model  ",
    )

    result = load_groq_settings(
        env_file=None,
    )

    assert result.api_key == "test-api-key"
    assert result.model == "test-model"


def test_load_groq_settings_rejects_missing_api_key(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv(
        "GROQ_API_KEY",
        raising=False,
    )
    monkeypatch.setenv(
        "GROQ_MODEL",
        "test-model",
    )

    with pytest.raises(
        ValueError,
        match="GROQ_API_KEY is not set",
    ):
        load_groq_settings(
            env_file=None,
        )


def test_load_groq_settings_rejects_missing_model(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(
        "GROQ_API_KEY",
        "test-api-key",
    )
    monkeypatch.delenv(
        "GROQ_MODEL",
        raising=False,
    )

    with pytest.raises(
        ValueError,
        match="GROQ_MODEL is not set",
    ):
        load_groq_settings(
            env_file=None,
        )
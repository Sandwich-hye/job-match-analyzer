import pytest
from pydantic import ValidationError

from app.extraction_models import (
    JobExtraction,
    WorkMode,
)
from app.extraction_prompt import (
    JOB_EXTRACTION_SYSTEM_PROMPT,
)
from app.job_extraction_service import (
    extract_job_information,
)


class FakeLLMClient:
    def __init__(
        self,
        response: str,
    ) -> None:
        self.response = response
        self.system_prompt: str | None = None
        self.user_prompt: str | None = None

    def generate(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt

        return self.response


def test_extract_job_information_returns_valid_model(
) -> None:
    client = FakeLLMClient(
        response="""
        {
          "job_title": "Software Engineer",
          "location": "Auckland",
          "work_mode": "hybrid",
          "requirements": []
        }
        """,
    )

    result = extract_job_information(
        job_description=(
            "We are hiring a hybrid "
            "Software Engineer in Auckland."
        ),
        client=client,
    )

    assert isinstance(result, JobExtraction)
    assert result.job_title == "Software Engineer"
    assert result.location == "Auckland"
    assert result.work_mode == WorkMode.HYBRID


def test_extract_job_information_sends_prompts_to_client(
) -> None:
    client = FakeLLMClient(
        response="""
        {
          "job_title": null,
          "location": null,
          "work_mode": "unknown",
          "requirements": []
        }
        """,
    )

    job_description = (
        "Strong Python experience is required."
    )

    extract_job_information(
        job_description=job_description,
        client=client,
    )

    assert (
        client.system_prompt
        == JOB_EXTRACTION_SYSTEM_PROMPT
    )

    assert client.user_prompt is not None

    assert job_description in client.user_prompt

    assert '"requirements"' in client.user_prompt


def test_extract_job_information_rejects_invalid_llm_output(
) -> None:
    client = FakeLLMClient(
        response="This is not valid JSON.",
    )

    with pytest.raises(ValidationError):
        extract_job_information(
            job_description=(
                "Python experience is required."
            ),
            client=client,
        )
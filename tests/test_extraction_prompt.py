import pytest

from app.extraction_prompt import (
    JOB_EXTRACTION_SYSTEM_PROMPT,
    build_job_extraction_prompt,
)


def test_system_prompt_requires_json_only_output() -> None:
    assert "Return only valid JSON" in (
        JOB_EXTRACTION_SYSTEM_PROMPT
    )

    assert "Do not include Markdown code fences" in (
        JOB_EXTRACTION_SYSTEM_PROMPT
    )


def test_build_prompt_includes_job_description() -> None:
    job_description = """
    We are hiring a Software Engineer.
    Strong Python experience is required.
    """

    result = build_job_extraction_prompt(
        job_description
    )

    assert (
        "We are hiring a Software Engineer."
        in result
    )
    assert (
        "Strong Python experience is required."
        in result
    )


def test_build_prompt_includes_json_schema_fields() -> None:
    result = build_job_extraction_prompt(
        "Python experience is required."
    )

    assert '"job_title"' in result
    assert '"location"' in result
    assert '"work_mode"' in result
    assert '"requirements"' in result
    assert '"job_evidence"' in result


def test_build_prompt_includes_allowed_enum_values() -> None:
    result = build_job_extraction_prompt(
        "This is a hybrid role."
    )

    assert '"onsite"' in result
    assert '"hybrid"' in result
    assert '"remote"' in result
    assert '"unknown"' in result

    assert '"required"' in result
    assert '"preferred"' in result


def test_build_prompt_strips_job_description() -> None:
    result = build_job_extraction_prompt(
        "   Python is required.   "
    )

    assert result.endswith(
        "Python is required."
    )


def test_build_prompt_rejects_empty_job_description(
) -> None:
    with pytest.raises(
        ValueError,
        match="job description must not be empty",
    ):
        build_job_extraction_prompt("   ")

def test_system_prompt_distinguishes_required_skills_from_blockers(
) -> None:
    normalized_prompt = " ".join(
        JOB_EXTRACTION_SYSTEM_PROMPT.split()
    )

    assert (
        "is not automatically an application blocker"
        in normalized_prompt
    )

    assert (
        "explicit eligibility condition"
        in normalized_prompt
    )

    assert (
        'Every application blocker must use '
        'category="feasibility"'
        in normalized_prompt
    )


def test_system_prompt_requests_normalized_requirement_names(
) -> None:
    assert (
        "Use concise, normalized requirement names"
        in JOB_EXTRACTION_SYSTEM_PROMPT
    )

def test_system_prompt_defines_requirement_categories(
) -> None:
    normalized_prompt = " ".join(
        JOB_EXTRACTION_SYSTEM_PROMPT.split()
    )

    assert (
        'Use "core_skill" for programming languages, '
        "frameworks, databases, cloud platforms"
        in normalized_prompt
    )

    assert (
        'Use "experience" for duration, seniority, scale, '
        "or depth of previous work"
        in normalized_prompt
    )

    assert (
        'Use "responsibility" for work the employee will '
        "be expected to perform"
        in normalized_prompt
    )

    assert (
        'Use "feasibility" for eligibility or practical '
        "constraints"
        in normalized_prompt
    )

    assert (
        'Do not use "bonus" merely because a requirement '
        "is preferred"
        in normalized_prompt
    )
import pytest
from pydantic import ValidationError

from app.extraction_models import (
    RequirementImportance,
    WorkMode,
)
from app.extraction_parser import (
    parse_job_extraction,
)
from app.models import RequirementCategory


def test_parse_job_extraction_returns_valid_model() -> None:
    raw_output = """
    {
      "job_title": "Software Engineer",
      "location": "Auckland",
      "work_mode": "hybrid",
      "requirements": [
        {
          "requirement": "Python",
          "category": "core_skill",
          "importance": "required",
          "job_evidence": "Python experience is required.",
          "is_application_blocker": false
        }
      ]
    }
    """

    result = parse_job_extraction(raw_output)

    assert result.job_title == "Software Engineer"
    assert result.location == "Auckland"
    assert result.work_mode == WorkMode.HYBRID

    assert len(result.requirements) == 1

    requirement = result.requirements[0]

    assert requirement.requirement == "Python"
    assert (
        requirement.category
        == RequirementCategory.CORE_SKILL
    )
    assert (
        requirement.importance
        == RequirementImportance.REQUIRED
    )
    assert requirement.is_application_blocker is False


def test_parse_job_extraction_rejects_empty_output() -> None:
    with pytest.raises(
        ValueError,
        match="LLM output must not be empty",
    ):
        parse_job_extraction("   ")


def test_parse_job_extraction_rejects_invalid_json() -> None:
    raw_output = """
    {
      "job_title": "Software Engineer",
    }
    """

    with pytest.raises(ValidationError):
        parse_job_extraction(raw_output)


def test_parse_job_extraction_rejects_invalid_schema() -> None:
    raw_output = """
    {
      "job_title": "Software Engineer",
      "work_mode": "sometimes_home",
      "requirements": []
    }
    """

    with pytest.raises(ValidationError):
        parse_job_extraction(raw_output)


def test_parse_job_extraction_rejects_duplicate_requirements(
) -> None:
    raw_output = """
    {
      "requirements": [
        {
          "requirement": "Python",
          "category": "core_skill",
          "importance": "required",
          "job_evidence": "Python is required."
        },
        {
          "requirement": "python",
          "category": "core_skill",
          "importance": "preferred",
          "job_evidence": "Python is preferred."
        }
      ]
    }
    """

    with pytest.raises(
        ValidationError,
        match="requirements must have unique names",
    ):
        parse_job_extraction(raw_output)
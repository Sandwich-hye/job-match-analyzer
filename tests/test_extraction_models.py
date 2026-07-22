import pytest
from pydantic import ValidationError

from app.extraction_models import (
    ExtractedRequirement,
    JobExtraction,
    RequirementImportance,
    WorkMode,
)
from app.models import RequirementCategory


def create_python_requirement(
    name: str = "Python",
) -> ExtractedRequirement:
    return ExtractedRequirement(
        requirement=name,
        category=RequirementCategory.CORE_SKILL,
        importance=RequirementImportance.REQUIRED,
        job_evidence=(
            "Strong Python experience is required."
        ),
    )


def test_job_extraction_accepts_valid_data() -> None:
    result = JobExtraction(
        job_title="Software Engineer",
        location="Auckland",
        work_mode=WorkMode.HYBRID,
        requirements=[
            create_python_requirement(),
        ],
    )

    assert result.job_title == "Software Engineer"
    assert result.location == "Auckland"
    assert result.work_mode == WorkMode.HYBRID
    assert len(result.requirements) == 1

    assert (
        result.requirements[0].importance
        == RequirementImportance.REQUIRED
    )


def test_extracted_requirement_strips_whitespace() -> None:
    result = ExtractedRequirement(
        requirement="  Python  ",
        category=RequirementCategory.CORE_SKILL,
        importance=RequirementImportance.REQUIRED,
        job_evidence="  - Python  ",
    )

    assert result.requirement == "Python"
    assert result.job_evidence == "- Python"


def test_job_extraction_uses_safe_defaults() -> None:
    result = JobExtraction()

    assert result.job_title is None
    assert result.location is None
    assert result.work_mode == WorkMode.UNKNOWN
    assert result.requirements == []


def test_extracted_requirement_rejects_empty_name() -> None:
    with pytest.raises(
        ValidationError,
        match="text must not be empty",
    ):
        ExtractedRequirement(
            requirement="   ",
            category=RequirementCategory.CORE_SKILL,
            importance=RequirementImportance.REQUIRED,
            job_evidence="- Python",
        )


def test_job_extraction_rejects_duplicate_requirements(
) -> None:
    with pytest.raises(
        ValidationError,
        match="requirements must have unique names",
    ):
        JobExtraction(
            requirements=[
                create_python_requirement("Python"),
                create_python_requirement("python"),
            ],
        )
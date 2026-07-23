from app.extraction_adapter import (
    adapt_extracted_requirement,
    build_requirement_matches_from_extraction,
)
from app.extraction_models import (
    ExtractedRequirement,
    JobExtraction,
    WorkMode,
)
from app.models import (
    MatchStatus,
    RequirementCategory,
    RequirementImportance,
)


def test_adapter_uses_catalog_aliases(
) -> None:
    extracted = ExtractedRequirement(
        requirement="AWS",
        category=(
            RequirementCategory.CORE_SKILL
        ),
        importance=(
            RequirementImportance.PREFERRED
        ),
        job_evidence=(
            "AWS experience is preferred."
        ),
        is_application_blocker=False,
    )

    result = adapt_extracted_requirement(
        extracted
    )

    assert result.name == "AWS"
    assert "Amazon Web Services" in (
        result.aliases
    )


def test_build_matches_finds_candidate_alias(
) -> None:
    extraction = JobExtraction(
        job_title="Software Engineer",
        location="Auckland, New Zealand",
        work_mode=WorkMode.HYBRID,
        requirements=[
            ExtractedRequirement(
                requirement="AWS",
                category=(
                    RequirementCategory
                    .CORE_SKILL
                ),
                importance=(
                    RequirementImportance
                    .PREFERRED
                ),
                job_evidence=(
                    "AWS experience is preferred."
                ),
                is_application_blocker=False,
            )
        ],
    )

    matches = (
        build_requirement_matches_from_extraction(
            extraction=extraction,
            resume=(
                "Cloud platforms: "
                "Amazon Web Services"
            ),
        )
    )

    assert len(matches) == 1
    assert (
        matches[0].status
        == MatchStatus.MATCHED
    )
    assert matches[0].requirement == "AWS"
    assert matches[0].candidate_evidence == (
        "Cloud platforms: Amazon Web Services"
    )
    assert matches[0].importance == (
        RequirementImportance.PREFERRED
    )


def test_build_matches_preserves_job_metadata(
) -> None:
    job_evidence = (
        "Applicants must have the legal "
        "right to work in New Zealand."
    )

    extraction = JobExtraction(
        job_title="Software Engineer",
        location="Auckland, New Zealand",
        work_mode=WorkMode.HYBRID,
        requirements=[
            ExtractedRequirement(
                requirement=(
                    "New Zealand work rights"
                ),
                category=(
                    RequirementCategory
                    .FEASIBILITY
                ),
                importance=(
                    RequirementImportance
                    .REQUIRED
                ),
                job_evidence=job_evidence,
                is_application_blocker=True,
            )
        ],
    )

    matches = (
        build_requirement_matches_from_extraction(
            extraction=extraction,
            resume=(
                "I hold unrestricted "
                "New Zealand work rights."
            ),
        )
    )

    assert len(matches) == 1
    assert (
        matches[0].status
        == MatchStatus.MATCHED
    )
    assert matches[0].job_evidence == (
        job_evidence
    )
    assert (
        matches[0].is_application_blocker
        is True
    )


def test_build_matches_supports_unknown_requirement(
) -> None:
    extraction = JobExtraction(
        job_title="Software Engineer",
        location=None,
        work_mode=WorkMode.UNKNOWN,
        requirements=[
            ExtractedRequirement(
                requirement=(
                    "Temporal workflow engine"
                ),
                category=(
                    RequirementCategory
                    .CORE_SKILL
                ),
                importance=(
                    RequirementImportance
                    .REQUIRED
                ),
                job_evidence=(
                    "Temporal workflow engine "
                    "experience is required."
                ),
                is_application_blocker=False,
            )
        ],
    )

    matches = (
        build_requirement_matches_from_extraction(
            extraction=extraction,
            resume=(
                "Built services using the "
                "Temporal workflow engine."
            ),
        )
    )

    assert len(matches) == 1
    assert matches[0].requirement == (
        "Temporal workflow engine"
    )
    assert (
        matches[0].status
        == MatchStatus.MATCHED
    )
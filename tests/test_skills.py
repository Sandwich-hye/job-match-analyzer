from app.skills import (
    KNOWN_REQUIREMENTS,
    KNOWN_SKILLS,
)
from app.analyzer import (
    analyse_job_match,
    build_requirement_matches,
    contains_skill,
    extract_requirement_evidence,
    extract_skill_evidence,
    find_matching_skills,
)
from app.models import (
    MatchStatus,
    RequirementCategory,
)
from app.skills import RequirementDefinition

def create_requirement_definition(
    name: str,
    aliases: tuple[str, ...] = (),
) -> RequirementDefinition:
    return RequirementDefinition(
        name=name,
        category=RequirementCategory.CORE_SKILL,
        aliases=aliases,
    )

def test_known_skills_are_derived_from_requirement_catalog() -> None:
    expected_skills = tuple(
        requirement.name
        for requirement in KNOWN_REQUIREMENTS
    )

    assert KNOWN_SKILLS == expected_skills


def test_requirement_catalog_has_unique_names() -> None:
    normalized_names = [
        requirement.name.casefold()
        for requirement in KNOWN_REQUIREMENTS
    ]

    assert len(normalized_names) == len(
        set(normalized_names)
    )


def test_aws_requirement_contains_full_name_alias() -> None:
    aws_requirement = next(
        requirement
        for requirement in KNOWN_REQUIREMENTS
        if requirement.name == "AWS"
    )

    assert "Amazon Web Services" in aws_requirement.aliases


def test_extract_requirement_evidence_matches_alias() -> None:
    requirement = create_requirement_definition(
        name="AWS",
        aliases=("Amazon Web Services",),
    )

    result = extract_requirement_evidence(
        "Experience with Amazon Web Services is required.",
        requirement,
    )

    assert result == (
        "Experience with Amazon Web Services is required."
    )

def test_analyse_job_match_normalizes_requirement_aliases() -> None:
    job_description = (
        "Experience with Amazon Web Services is required."
    )
    resume = "Built and deployed applications using AWS."

    requirements = (
        create_requirement_definition(
            name="AWS",
            aliases=("Amazon Web Services",),
        ),
    )

    result = analyse_job_match(
        job_description,
        resume,
        requirements,
    )

    assert result.matched_skills == ["AWS"]
    assert result.missing_skills == []

    assert len(result.requirement_matches) == 1

    requirement_match = result.requirement_matches[0]

    assert requirement_match.requirement == "AWS"
    assert requirement_match.status == MatchStatus.MATCHED
    assert requirement_match.job_evidence == (
        "Experience with Amazon Web Services is required."
    )
    assert requirement_match.candidate_evidence == (
        "Built and deployed applications using AWS."
    )
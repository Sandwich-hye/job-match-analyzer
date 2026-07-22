from app.analyzer import (
    analyse_job_match,
    build_requirement_matches,
    contains_skill,
    extract_requirement_evidence,
    extract_skill_evidence,
)
from app.models import (
    MatchStatus,
    RequirementCategory,
)
from app.skills import RequirementDefinition


def create_requirement_definition(
    name: str,
    *,
    aliases: tuple[str, ...] = (),
    category: RequirementCategory = (
        RequirementCategory.CORE_SKILL
    ),
    is_application_blocker: bool = False,
) -> RequirementDefinition:
    return RequirementDefinition(
        name=name,
        category=category,
        aliases=aliases,
        is_application_blocker=is_application_blocker,
    )

def test_contains_skill_matches_complete_skill_name() -> None:
    result = contains_skill(
        "The candidate has strong Python experience.",
        "Python",
    )

    assert result is True


def test_contains_skill_is_case_insensitive() -> None:
    result = contains_skill(
        "The candidate has PYTHON experience.",
        "python",
    )

    assert result is True


def test_contains_skill_does_not_match_partial_word() -> None:
    result = contains_skill(
        "The candidate has JavaScript experience.",
        "Java",
    )

    assert result is False


def test_contains_skill_matches_c_plus_plus() -> None:
    assert contains_skill(
        "Experience with C++ development.",
        "C++",
    ) is True


def test_contains_skill_does_not_match_c_plus_plus_inside_longer_text(
) -> None:
    assert contains_skill(
        "Experience with XC++Tools.",
        "C++",
    ) is False


def test_analyse_job_match_returns_structured_result() -> None:
    job_description = "Python SQL Git Docker"
    resume = "Python SQL Git"

    requirements = (
        create_requirement_definition("Python"),
        create_requirement_definition("SQL"),
        create_requirement_definition("Git"),
        create_requirement_definition("Docker"),
    )

    result = analyse_job_match(
        job_description,
        resume,
        requirements,
    )

    assert result.matched_skills == [
        "Python",
        "SQL",
        "Git",
    ]
    assert result.missing_skills == ["Docker"]

    assert result.requirement_score == 75.0
    assert result.match_score == 75.0

    assert [
        item.requirement
        for item in result.requirement_matches
    ] == [
        "Python",
        "SQL",
        "Git",
        "Docker",
    ]

    assert [
        item.status
        for item in result.requirement_matches
    ] == [
        MatchStatus.MATCHED,
        MatchStatus.MATCHED,
        MatchStatus.MATCHED,
        MatchStatus.NOT_ENOUGH_INFORMATION,
    ]

    assert result.category_scores == {
        RequirementCategory.CORE_SKILL: 75.0,
    }


def test_build_requirement_matches_returns_status_for_each_required_skill(
) -> None:
    job_description = "Python and Docker are required."
    resume = "Experienced Python developer."

    requirements = (
        create_requirement_definition("Python"),
        create_requirement_definition("Docker"),
        create_requirement_definition("React"),
    )

    result = build_requirement_matches(
        job_description,
        resume,
        requirements,
    )

    assert len(result) == 2

    assert result[0].requirement == "Python"
    assert result[0].category == RequirementCategory.CORE_SKILL
    assert result[0].status == MatchStatus.MATCHED
    assert result[0].job_evidence == (
        "Python and Docker are required."
    )
    assert result[0].candidate_evidence == (
        "Experienced Python developer."
    )

    assert result[1].requirement == "Docker"
    assert result[1].category == RequirementCategory.CORE_SKILL
    assert (
        result[1].status
        == MatchStatus.NOT_ENOUGH_INFORMATION
    )
    assert result[1].job_evidence == (
        "Python and Docker are required."
    )
    assert result[1].candidate_evidence is None


def test_build_requirement_matches_ignores_skills_not_required_by_job(
) -> None:
    job_description = "Python is required."
    resume = "Experienced with Python and React."

    requirements = (
        create_requirement_definition("Python"),
        create_requirement_definition("Docker"),
        create_requirement_definition("React"),
    )

    result = build_requirement_matches(
        job_description,
        resume,
        requirements,
    )

    assert [
        requirement_match.requirement
        for requirement_match in result
    ] == ["Python"]


def test_extract_skill_evidence_returns_matching_line() -> None:
    resume = """
    Skills:
    - Python
    - SQL
    """

    result = extract_skill_evidence(
        resume,
        "Python",
    )

    assert result == "- Python"


def test_extract_skill_evidence_is_case_insensitive() -> None:
    resume = """
    Experience:
    Built backend services using PYTHON and FastAPI.
    """

    result = extract_skill_evidence(
        resume,
        "python",
    )

    assert result == (
        "Built backend services using PYTHON and FastAPI."
    )


def test_extract_skill_evidence_returns_none_when_not_found() -> None:
    resume = """
    Skills:
    - React
    - TypeScript
    """

    result = extract_skill_evidence(
        resume,
        "Docker",
    )

    assert result is None


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
    assert result.requirement_score == 100.0
    assert result.match_score == 100.0

    assert len(result.requirement_matches) == 1

    requirement_match = result.requirement_matches[0]

    assert requirement_match.requirement == "AWS"
    assert requirement_match.category == (
        RequirementCategory.CORE_SKILL
    )
    assert requirement_match.status == MatchStatus.MATCHED
    assert requirement_match.job_evidence == (
        "Experience with Amazon Web Services is required."
    )
    assert requirement_match.candidate_evidence == (
        "Built and deployed applications using AWS."
    )

def test_analyse_job_match_surfaces_unmet_application_blocker(
) -> None:
    job_description = """
    Requirements:
    - New Zealand citizenship
    - Python
    """

    resume = """
    Skills:
    - Python
    """

    requirements = (
        create_requirement_definition(
            "New Zealand citizenship",
            category=RequirementCategory.FEASIBILITY,
            is_application_blocker=True,
        ),
        create_requirement_definition("Python"),
    )

    result = analyse_job_match(
        job_description,
        resume,
        requirements,
    )

    assert result.potential_application_blockers == [
        "New Zealand citizenship",
    ]


def test_analyse_job_match_does_not_surface_matched_blocker(
) -> None:
    job_description = """
    Requirements:
    - New Zealand citizenship
    """

    resume = """
    Eligibility:
    - New Zealand citizenship
    """

    requirements = (
        create_requirement_definition(
            "New Zealand citizenship",
            category=RequirementCategory.FEASIBILITY,
            is_application_blocker=True,
        ),
    )

    result = analyse_job_match(
        job_description,
        resume,
        requirements,
    )

    assert result.potential_application_blockers == []
from app.analyzer import (
    analyse_job_match,
    build_requirement_matches,
    contains_skill,
    extract_skill_evidence,
    find_matching_skills,
)
from app.models import (
    MatchStatus,
    RequirementCategory,
)

def test_find_matching_skills_returns_matched_and_missing_skills() -> None:
    job_description = """
    Requirements:
    - Python
    - SQL
    - Git
    - Docker
    """

    resume = """
    Skills:
    - Python
    - SQL
    - Git
    """

    known_skills = [
        "Python",
        "SQL",
        "Git",
        "Docker",
        "React",
    ]

    matched_skills, missing_skills = find_matching_skills(
        job_description,
        resume,
        known_skills,
    )

    assert matched_skills == ["Python", "SQL", "Git"]
    assert missing_skills == ["Docker"]


def test_find_matching_skills_is_case_insensitive() -> None:
    job_description = "python sql docker"
    resume = "PYTHON Sql"
    known_skills = ["Python", "SQL", "Docker"]

    matched_skills, missing_skills = find_matching_skills(
        job_description,
        resume,
        known_skills,
    )

    assert matched_skills == ["Python", "SQL"]
    assert missing_skills == ["Docker"]


def test_find_matching_skills_returns_empty_lists_when_jd_has_no_known_skills(
) -> None:
    job_description = "Excellent communication and teamwork required."
    resume = "Experienced software developer."
    known_skills = ["Python", "SQL", "Docker"]

    matched_skills, missing_skills = find_matching_skills(
        job_description,
        resume,
        known_skills,
    )

    assert matched_skills == []
    assert missing_skills == []


def test_find_matching_skills_returns_no_missing_skills_when_all_match(
) -> None:
    job_description = "Python SQL Git"
    resume = "Python SQL Git Docker"
    known_skills = ["Python", "SQL", "Git", "Docker"]

    matched_skills, missing_skills = find_matching_skills(
        job_description,
        resume,
        known_skills,
    )

    assert matched_skills == ["Python", "SQL", "Git"]
    assert missing_skills == []


def test_find_matching_skills_returns_all_required_skills_as_missing(
) -> None:
    job_description = "Python SQL Docker"
    resume = "React TypeScript"
    known_skills = [
        "Python",
        "SQL",
        "Docker",
        "React",
        "TypeScript",
    ]

    matched_skills, missing_skills = find_matching_skills(
        job_description,
        resume,
        known_skills,
    )

    assert matched_skills == []
    assert missing_skills == ["Python", "SQL", "Docker"]

def test_find_matching_skills_does_not_match_java_inside_javascript() -> None:
    job_description = "Java developer required."
    resume = "Experienced JavaScript developer."
    known_skills = ["Java", "JavaScript"]

    matched_skills, missing_skills = find_matching_skills(
        job_description,
        resume,
        known_skills,
    )

    assert matched_skills == []
    assert missing_skills == ["Java"]


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

def test_contains_skill_does_not_match_c_plus_plus_inside_longer_text() -> None:
    assert contains_skill(
        "Experience with XC++Tools.",
        "C++",
    ) is False

def test_analyse_job_match_returns_structured_result() -> None:
    job_description = "Python SQL Git Docker"
    resume = "Python SQL Git"
    known_skills = [
        "Python",
        "SQL",
        "Git",
        "Docker",
    ]

    result = analyse_job_match(
        job_description,
        resume,
        known_skills,
    )

    assert result.matched_skills == [
        "Python",
        "SQL",
        "Git",
    ]
    assert result.missing_skills == ["Docker"]
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

    assert result.requirement_score == 75.0
    assert result.match_score == 75.0


def test_build_requirement_matches_returns_status_for_each_required_skill(
) -> None:
    job_description = "Python and Docker are required."
    resume = "Experienced Python developer."
    known_skills = (
        "Python",
        "Docker",
        "React",
    )

    result = build_requirement_matches(
        job_description,
        resume,
        known_skills,
    )

    assert len(result) == 2

    assert result[0].requirement == "Python"
    assert result[0].status == MatchStatus.MATCHED
    assert result[0].candidate_evidence == (
        "Experienced Python developer."
    )
    assert result[1].requirement == "Docker"
    assert result[1].status == MatchStatus.NOT_ENOUGH_INFORMATION
    assert result[1].candidate_evidence is None
    assert result[0].job_evidence == (
        "Python and Docker are required."
    )

def test_build_requirement_matches_ignores_skills_not_required_by_job(
) -> None:
    job_description = "Python is required."
    resume = "Experienced with Python and React."
    known_skills = (
        "Python",
        "Docker",
        "React",
    )

    result = build_requirement_matches(
        job_description,
        resume,
        known_skills,
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

    assert result == "Built backend services using PYTHON and FastAPI."


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
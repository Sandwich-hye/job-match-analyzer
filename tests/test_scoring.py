from app.models import (
    MatchStatus,
    RequirementCategory,
    RequirementMatch,
)
from app.scoring import (
    calculate_category_scores,
    calculate_requirement_score,
)

def create_requirement_match(
    requirement: str,
    status: MatchStatus,
    category: RequirementCategory = RequirementCategory.CORE_SKILL,
) -> RequirementMatch:
    return RequirementMatch(
        requirement=requirement,
        category=category,
        status=status,
        job_evidence=f"- {requirement}",
    )

def test_calculate_requirement_score_returns_correct_score() -> None:
    requirement_matches = [
        create_requirement_match(
            "Python",
            MatchStatus.MATCHED,
        ),
        create_requirement_match(
            "SQL",
            MatchStatus.MATCHED,
        ),
        create_requirement_match(
            "Docker",
            MatchStatus.PARTIALLY_MATCHED,
        ),
        create_requirement_match(
            "AWS",
            MatchStatus.NOT_ENOUGH_INFORMATION,
        ),
    ]

    result = calculate_requirement_score(requirement_matches)

    assert result == 62.5


def test_calculate_requirement_score_returns_100_when_all_match() -> None:
    requirement_matches = [
        create_requirement_match(
            "Python",
            MatchStatus.MATCHED,
        ),
        create_requirement_match(
            "SQL",
            MatchStatus.MATCHED,
        ),
    ]

    result = calculate_requirement_score(requirement_matches)

    assert result == 100.0


def test_calculate_requirement_score_returns_zero_when_none_match() -> None:
    requirement_matches = [
        create_requirement_match(
            "Docker",
            MatchStatus.NOT_MATCHED,
        ),
        create_requirement_match(
            "AWS",
            MatchStatus.NOT_ENOUGH_INFORMATION,
        ),
    ]

    result = calculate_requirement_score(requirement_matches)

    assert result == 0.0


def test_calculate_requirement_score_returns_zero_for_empty_input() -> None:
    result = calculate_requirement_score([])

    assert result == 0.0

def test_calculate_category_scores_groups_requirements_by_category(
) -> None:
    requirement_matches = [
        create_requirement_match(
            "Python",
            MatchStatus.MATCHED,
            RequirementCategory.CORE_SKILL,
        ),
        create_requirement_match(
            "Docker",
            MatchStatus.PARTIALLY_MATCHED,
            RequirementCategory.CORE_SKILL,
        ),
        create_requirement_match(
            "Three years of backend experience",
            MatchStatus.MATCHED,
            RequirementCategory.EXPERIENCE,
        ),
        create_requirement_match(
            "Five years of commercial experience",
            MatchStatus.NOT_ENOUGH_INFORMATION,
            RequirementCategory.EXPERIENCE,
        ),
        create_requirement_match(
            "AWS certification",
            MatchStatus.MATCHED,
            RequirementCategory.BONUS,
        ),
    ]

    result = calculate_category_scores(requirement_matches)

    assert result == {
        RequirementCategory.CORE_SKILL: 75.0,
        RequirementCategory.EXPERIENCE: 50.0,
        RequirementCategory.BONUS: 100.0,
    }


def test_calculate_category_scores_returns_empty_dict_for_empty_input(
) -> None:
    result = calculate_category_scores([])

    assert result == {}


def test_calculate_category_scores_returns_zero_when_category_has_no_match(
) -> None:
    requirement_matches = [
        create_requirement_match(
            "Security clearance",
            MatchStatus.NOT_ENOUGH_INFORMATION,
            RequirementCategory.FEASIBILITY,
        ),
    ]

    result = calculate_category_scores(requirement_matches)

    assert result == {
        RequirementCategory.FEASIBILITY: 0.0,
    }
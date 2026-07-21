from app.models import (
    MatchStatus,
    RequirementCategory,
    RequirementMatch,
)
from app.scoring import calculate_requirement_score


def create_requirement_match(
    requirement: str,
    status: MatchStatus,
) -> RequirementMatch:
    return RequirementMatch(
        requirement=requirement,
        category=RequirementCategory.CORE_SKILL,
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
from collections.abc import Sequence

from app.models import (
    MatchStatus,
    RequirementCategory,
    RequirementMatch,
)

STATUS_SCORES: dict[MatchStatus, float] = {
    MatchStatus.MATCHED: 1.0,
    MatchStatus.PARTIALLY_MATCHED: 0.5,
    MatchStatus.NOT_MATCHED: 0.0,
    MatchStatus.NOT_ENOUGH_INFORMATION: 0.0,
}


def calculate_requirement_score(
    requirement_matches: Sequence[RequirementMatch],
) -> float:
    if not requirement_matches:
        return 0.0

    earned_score = sum(
        STATUS_SCORES[item.status]
        for item in requirement_matches
    )

    score = earned_score / len(requirement_matches) * 100

    return round(score, 2)


def calculate_category_scores(
    requirement_matches: Sequence[RequirementMatch],
) -> dict[RequirementCategory, float]:
    scores_by_category: dict[
        RequirementCategory,
        list[float],
    ] = {}

    for item in requirement_matches:
        scores_by_category.setdefault(
            item.category,
            [],
        ).append(
            STATUS_SCORES[item.status]
        )

    return {
        category: round(
            sum(scores) / len(scores) * 100,
            2,
        )
        for category, scores in scores_by_category.items()
    }
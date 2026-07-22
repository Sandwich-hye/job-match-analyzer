from collections.abc import Mapping, Sequence

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

CATEGORY_WEIGHTS: dict[RequirementCategory, float] = {
    RequirementCategory.CORE_SKILL: 0.35,
    RequirementCategory.EXPERIENCE: 0.25,
    RequirementCategory.RESPONSIBILITY: 0.20,
    RequirementCategory.BONUS: 0.10,
    RequirementCategory.FEASIBILITY: 0.10,
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

def calculate_weighted_score(
    category_scores: Mapping[RequirementCategory, float],
    category_weights: Mapping[RequirementCategory, float] | None = None,
) -> float:
    if not category_scores:
        return 0.0

    weights = (
        CATEGORY_WEIGHTS
        if category_weights is None
        else category_weights
    )

    for category, score in category_scores.items():
        if category not in weights:
            raise ValueError(
                f"Missing weight for category: {category.value}"
            )

        if not 0 <= score <= 100:
            raise ValueError(
                f"Category score must be between 0 and 100: "
                f"{category.value}={score}"
            )

    active_weight_total = sum(
        weights[category]
        for category in category_scores
    )

    if active_weight_total <= 0:
        raise ValueError(
            "The total active category weight must be greater than zero."
        )

    weighted_score = sum(
        score * weights[category]
        for category, score in category_scores.items()
    )

    normalized_score = weighted_score / active_weight_total

    return round(normalized_score, 2)
from collections.abc import Sequence

from app.models import Recommendation


APPLY_THRESHOLD = 75.0
CONSIDER_THRESHOLD = 50.0


def determine_recommendation(
    match_score: float,
    potential_application_blockers: Sequence[str],
) -> Recommendation:
    if not 0 <= match_score <= 100:
        raise ValueError(
            "match_score must be between 0 and 100"
        )

    if potential_application_blockers:
        return Recommendation.CONSIDER

    if match_score >= APPLY_THRESHOLD:
        return Recommendation.APPLY

    if match_score >= CONSIDER_THRESHOLD:
        return Recommendation.CONSIDER

    return Recommendation.SKIP
import pytest

from app.models import Recommendation
from app.recommendation import determine_recommendation


def test_recommendation_is_apply_for_high_score_without_blockers(
) -> None:
    result = determine_recommendation(
        match_score=80.0,
        potential_application_blockers=[],
    )

    assert result == Recommendation.APPLY


def test_recommendation_is_consider_when_blocker_exists(
) -> None:
    result = determine_recommendation(
        match_score=90.0,
        potential_application_blockers=[
            "New Zealand citizenship",
        ],
    )

    assert result == Recommendation.CONSIDER


def test_recommendation_is_apply_at_apply_threshold() -> None:
    result = determine_recommendation(
        match_score=75.0,
        potential_application_blockers=[],
    )

    assert result == Recommendation.APPLY


def test_recommendation_is_consider_at_consider_threshold(
) -> None:
    result = determine_recommendation(
        match_score=50.0,
        potential_application_blockers=[],
    )

    assert result == Recommendation.CONSIDER


def test_recommendation_is_skip_below_consider_threshold(
) -> None:
    result = determine_recommendation(
        match_score=49.9,
        potential_application_blockers=[],
    )

    assert result == Recommendation.SKIP


@pytest.mark.parametrize(
    "invalid_score",
    [-0.1, 100.1],
)
def test_recommendation_rejects_invalid_score(
    invalid_score: float,
) -> None:
    with pytest.raises(
        ValueError,
        match="match_score must be between 0 and 100",
    ):
        determine_recommendation(
            match_score=invalid_score,
            potential_application_blockers=[],
        )
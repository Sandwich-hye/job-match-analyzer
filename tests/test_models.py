import pytest
from pydantic import ValidationError

from app.models import MatchResult


def test_match_result_accepts_valid_data() -> None:
    result = MatchResult(
        matched_skills=["Python", "SQL"],
        missing_skills=["Docker"],
        match_score=66.67,
    )

    assert result.matched_skills == ["Python", "SQL"]
    assert result.missing_skills == ["Docker"]
    assert result.match_score == 66.67


def test_match_result_rejects_score_below_zero() -> None:
    with pytest.raises(ValidationError):
        MatchResult(
            matched_skills=[],
            missing_skills=["Python"],
            match_score=-1,
        )


def test_match_result_rejects_score_above_100() -> None:
    with pytest.raises(ValidationError):
        MatchResult(
            matched_skills=["Python"],
            missing_skills=[],
            match_score=101,
        )
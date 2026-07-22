import pytest
from pydantic import ValidationError

from app.models import (
    MatchResult,
    MatchStatus,
    RequirementCategory,
    RequirementMatch,
)


def test_match_result_accepts_valid_data() -> None:
    result = MatchResult(
        matched_skills=["Python", "SQL"],
        missing_skills=["Docker"],
        requirement_score=66.67,
        match_score=66.67,
    )

    assert result.matched_skills == ["Python", "SQL"]
    assert result.missing_skills == ["Docker"]
    assert result.requirement_score == 66.67
    assert result.match_score == 66.67


def test_match_result_rejects_score_below_zero() -> None:
    with pytest.raises(ValidationError):
        MatchResult(
            matched_skills=[],
            missing_skills=["Python"],
            requirement_score=0.0,
            match_score=-1,
        )


def test_match_result_rejects_score_above_100() -> None:
    with pytest.raises(ValidationError):
        MatchResult(
            matched_skills=["Python"],
            missing_skills=[],
            requirement_score=100.0,
            match_score=101,
        )


def test_requirement_match_accepts_valid_data() -> None:
    result = RequirementMatch(
        requirement="Python",
        category=RequirementCategory.CORE_SKILL,
        status=MatchStatus.MATCHED,
        job_evidence="- Python",
        candidate_evidence=(
            "Python listed in the Skills section."
        ),
        is_application_blocker=False,
    )

    assert result.requirement == "Python"
    assert result.category == RequirementCategory.CORE_SKILL
    assert result.status == MatchStatus.MATCHED
    assert result.job_evidence == "- Python"
    assert result.candidate_evidence == (
        "Python listed in the Skills section."
    )
    assert result.is_application_blocker is False


def test_requirement_match_allows_missing_candidate_evidence() -> None:
    result = RequirementMatch(
        requirement="Docker",
        category=RequirementCategory.CORE_SKILL,
        status=MatchStatus.NOT_ENOUGH_INFORMATION,
        job_evidence="- Docker",
    )

    assert result.category == RequirementCategory.CORE_SKILL
    assert result.job_evidence == "- Docker"
    assert result.candidate_evidence is None
    assert result.is_application_blocker is False


def test_requirement_match_rejects_invalid_status() -> None:
    with pytest.raises(ValidationError):
        RequirementMatch(
            requirement="Python",
            category=RequirementCategory.CORE_SKILL,
            status="complete_match",
            job_evidence="- Python",
        )


def test_match_result_defaults_requirement_matches_to_empty_list() -> None:
    result = MatchResult(
        matched_skills=["Python"],
        missing_skills=["Docker"],
        requirement_score=50.0,
        match_score=50.0,
    )

    assert result.requirement_matches == []


def test_requirement_match_requires_job_evidence() -> None:
    with pytest.raises(ValidationError):
        RequirementMatch(
            requirement="Python",
            category=RequirementCategory.CORE_SKILL,
            status=MatchStatus.MATCHED,
            candidate_evidence="- Python",
        )


def test_requirement_match_rejects_invalid_category() -> None:
    with pytest.raises(ValidationError):
        RequirementMatch(
            requirement="Python",
            category="technical_thing",
            status=MatchStatus.MATCHED,
            job_evidence="- Python",
        )

def test_match_result_defaults_category_scores_to_empty_dict() -> None:
    result = MatchResult(
        matched_skills=["Python"],
        missing_skills=["Docker"],
        requirement_score=50.0,
        match_score=50.0,
    )

    assert result.category_scores == {}

def test_match_result_rejects_invalid_requirement_score() -> None:
    with pytest.raises(ValidationError):
        MatchResult(
            matched_skills=[],
            missing_skills=["Python"],
            requirement_score=120.0,
            match_score=0.0,
        )
import pytest
from pydantic import ValidationError
from app.models import RequirementImportance
from app.models import (
    MatchResult,
    MatchStatus,
    Recommendation,
    RequirementCategory,
    RequirementMatch,
)


def test_match_result_accepts_valid_data() -> None:
    result = MatchResult(
        matched_skills=["Python", "SQL"],
        missing_skills=["Docker"],
        requirement_score=66.67,
        match_score=66.67,
        recommendation=Recommendation.CONSIDER,
    )

    assert result.matched_skills == ["Python", "SQL"]
    assert result.missing_skills == ["Docker"]
    assert result.requirement_score == 66.67
    assert result.match_score == 66.67
    assert result.recommendation == Recommendation.CONSIDER


def test_match_result_rejects_score_below_zero() -> None:
    with pytest.raises(ValidationError):
        MatchResult(
            matched_skills=[],
            missing_skills=["Python"],
            requirement_score=0.0,
            match_score=-1,
            recommendation=Recommendation.SKIP,
        )


def test_match_result_rejects_score_above_100() -> None:
    with pytest.raises(ValidationError):
        MatchResult(
            matched_skills=["Python"],
            missing_skills=[],
            requirement_score=100.0,
            match_score=101,
            recommendation=Recommendation.APPLY,
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
        recommendation=Recommendation.CONSIDER,
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
        recommendation=Recommendation.CONSIDER,
    )

    assert result.category_scores == {}


def test_match_result_defaults_potential_blockers_to_empty_list() -> None:
    result = MatchResult(
        matched_skills=["Python"],
        missing_skills=["Docker"],
        requirement_score=50.0,
        match_score=50.0,
        recommendation=Recommendation.CONSIDER,
    )

    assert result.potential_application_blockers == []


def test_match_result_rejects_invalid_requirement_score() -> None:
    with pytest.raises(ValidationError):
        MatchResult(
            matched_skills=[],
            missing_skills=["Python"],
            requirement_score=120.0,
            match_score=0.0,
            recommendation=Recommendation.SKIP,
        )


def test_match_result_rejects_invalid_recommendation() -> None:
    with pytest.raises(ValidationError):
        MatchResult(
            matched_skills=["Python"],
            missing_skills=[],
            requirement_score=100.0,
            match_score=100.0,
            recommendation="definitely_apply",
        )


def test_requirement_match_accepts_preferred_importance(
) -> None:
    result = RequirementMatch(
        requirement="AWS",
        category=RequirementCategory.CORE_SKILL,
        importance=RequirementImportance.PREFERRED,
        status=MatchStatus.NOT_MATCHED,
        job_evidence="AWS experience is preferred.",
    )

    assert (
        result.importance
        == RequirementImportance.PREFERRED
    )

def test_requirement_match_defaults_importance_to_required(
) -> None:
    result = RequirementMatch(
        requirement="Python",
        category=RequirementCategory.CORE_SKILL,
        status=MatchStatus.MATCHED,
        job_evidence="Python is required.",
        candidate_evidence="Skills: Python",
    )

    assert (
        result.importance
        == RequirementImportance.REQUIRED
    )
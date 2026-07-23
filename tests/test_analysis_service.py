import json

from app.analysis_service import (
    analyse_job_match_with_llm,
)
from app.models import (
    Recommendation,
    RequirementCategory,
)


class FakeLLMClient:
    def __init__(
        self,
        output: str,
    ) -> None:
        self.output = output

    def generate(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        response_schema: (
            dict[str, object] | None
        ) = None,
    ) -> str:
        return self.output


def test_analysis_service_returns_apply_when_all_match(
) -> None:
    raw_output = json.dumps(
        {
            "job_title": "Software Engineer",
            "location": "Auckland",
            "work_mode": "hybrid",
            "requirements": [
                {
                    "requirement": "Python",
                    "category": "core_skill",
                    "importance": "required",
                    "job_evidence": (
                        "Python is required."
                    ),
                    "is_application_blocker": False,
                },
                {
                    "requirement": (
                        "New Zealand work rights"
                    ),
                    "category": "feasibility",
                    "importance": "required",
                    "job_evidence": (
                        "Applicants must have "
                        "New Zealand work rights."
                    ),
                    "is_application_blocker": True,
                },
            ],
        }
    )

    client = FakeLLMClient(raw_output)

    result = analyse_job_match_with_llm(
        job_description="Example job description",
        resume=(
            "Skills: Python\n"
            "I have unrestricted "
            "New Zealand work rights."
        ),
        client=client,
    )

    assert result.match_score == 100.0
    assert result.requirement_score == 100.0
    assert result.recommendation == (
        Recommendation.APPLY
    )
    assert (
        result.potential_application_blockers
        == []
    )


def test_analysis_service_returns_consider_for_blocker(
) -> None:
    raw_output = json.dumps(
        {
            "job_title": "Software Engineer",
            "location": "Auckland",
            "work_mode": "hybrid",
            "requirements": [
                {
                    "requirement": "Python",
                    "category": "core_skill",
                    "importance": "required",
                    "job_evidence": (
                        "Python is required."
                    ),
                    "is_application_blocker": False,
                },
                {
                    "requirement": (
                        "New Zealand work rights"
                    ),
                    "category": "feasibility",
                    "importance": "required",
                    "job_evidence": (
                        "Applicants must have "
                        "New Zealand work rights."
                    ),
                    "is_application_blocker": True,
                },
            ],
        }
    )

    client = FakeLLMClient(raw_output)

    result = analyse_job_match_with_llm(
        job_description="Example job description",
        resume="Skills: Python",
        client=client,
    )

    assert result.recommendation == (
        Recommendation.CONSIDER
    )

    assert result.potential_application_blockers == [
        "New Zealand work rights"
    ]

    assert "New Zealand work rights" in (
        result.missing_skills
    )


def test_analysis_service_uses_importance_weight(
) -> None:
    raw_output = json.dumps(
        {
            "job_title": "Software Engineer",
            "location": "Auckland",
            "work_mode": "hybrid",
            "requirements": [
                {
                    "requirement": "Python",
                    "category": "core_skill",
                    "importance": "required",
                    "job_evidence": (
                        "Python is required."
                    ),
                    "is_application_blocker": False,
                },
                {
                    "requirement": "AWS",
                    "category": "core_skill",
                    "importance": "preferred",
                    "job_evidence": (
                        "AWS is preferred."
                    ),
                    "is_application_blocker": False,
                },
            ],
        }
    )

    client = FakeLLMClient(raw_output)

    result = analyse_job_match_with_llm(
        job_description="Example job description",
        resume=(
            "Cloud: Amazon Web Services"
        ),
        client=client,
    )

    assert result.category_scores[
        RequirementCategory.CORE_SKILL
    ] == 33.33

    assert result.requirement_score == 33.33
    assert result.match_score == 33.33
    assert result.recommendation == (
        Recommendation.SKIP
    )
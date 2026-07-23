from app.analyzer import (
    find_potential_application_blockers,
)
from app.extraction_adapter import (
    build_requirement_matches_from_extraction,
)
from app.job_extraction_service import (
    extract_job_information,
)
from app.llm_client import LLMClient
from app.models import (
    MatchResult,
    MatchStatus,
)
from app.recommendation import (
    determine_recommendation,
)
from app.scoring import (
    calculate_category_scores,
    calculate_requirement_score,
    calculate_weighted_score,
)


def analyse_job_match_with_llm(
    job_description: str,
    resume: str,
    client: LLMClient,
) -> MatchResult:
    extraction = extract_job_information(
        job_description=job_description,
        client=client,
    )

    requirement_matches = (
        build_requirement_matches_from_extraction(
            extraction=extraction,
            resume=resume,
        )
    )

    matched_skills = [
        item.requirement
        for item in requirement_matches
        if item.status == MatchStatus.MATCHED
    ]

    missing_skills = [
        item.requirement
        for item in requirement_matches
        if item.status
        in {
            MatchStatus.NOT_MATCHED,
            MatchStatus.NOT_ENOUGH_INFORMATION,
        }
    ]

    potential_application_blockers = (
        find_potential_application_blockers(
            requirement_matches
        )
    )

    requirement_score = (
        calculate_requirement_score(
            requirement_matches
        )
    )

    category_scores = calculate_category_scores(
        requirement_matches
    )

    match_score = calculate_weighted_score(
        category_scores
    )

    recommendation = determine_recommendation(
        match_score=match_score,
        potential_application_blockers=(
            potential_application_blockers
        ),
    )

    return MatchResult(
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        requirement_score=requirement_score,
        match_score=match_score,
        recommendation=recommendation,
        category_scores=category_scores,
        requirement_matches=requirement_matches,
        potential_application_blockers=(
            potential_application_blockers
        ),
    )
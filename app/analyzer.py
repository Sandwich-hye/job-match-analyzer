import re
from collections.abc import Sequence

from app.models import (
    MatchResult,
    MatchStatus,
    RequirementMatch,
)
from app.scoring import (
    calculate_category_scores,
    calculate_requirement_score,
    calculate_weighted_score,
)
from app.skills import RequirementDefinition

def contains_skill(text: str, skill: str) -> bool:
    escaped_skill = re.escape(skill)

    pattern = rf"(?<!\w){escaped_skill}(?!\w)"

    return re.search(
        pattern,
        text,
        flags=re.IGNORECASE,
    ) is not None

def analyse_job_match(
    job_description: str,
    resume: str,
    requirements: Sequence[RequirementDefinition],
) -> MatchResult:
    requirement_matches = build_requirement_matches(
        job_description,
        resume,
        requirements,
    )

    matched_skills = [
        item.requirement
        for item in requirement_matches
        if item.status == MatchStatus.MATCHED
    ]

    missing_skills = [
        item.requirement
        for item in requirement_matches
        if item.status in {
            MatchStatus.NOT_MATCHED,
            MatchStatus.NOT_ENOUGH_INFORMATION,
        }
    ]

    requirement_score = calculate_requirement_score(
        requirement_matches,
    )

    category_scores = calculate_category_scores(
        requirement_matches,
    )

    match_score = calculate_weighted_score(
        category_scores,
    )

    return MatchResult(
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        requirement_score=requirement_score,
        match_score=match_score,
        category_scores=category_scores,
        requirement_matches=requirement_matches,
    )

def build_requirement_matches(
    job_description: str,
    resume: str,
    requirements: Sequence[RequirementDefinition],
) -> list[RequirementMatch]:
    requirement_matches: list[RequirementMatch] = []

    for requirement in requirements:
        job_evidence = extract_requirement_evidence(
            job_description,
            requirement,
        )

        if job_evidence is None:
            continue

        candidate_evidence = extract_requirement_evidence(
            resume,
            requirement,
        )

        requirement_matches.append(
            RequirementMatch(
                requirement=requirement.name,
                category=requirement.category,
                status=(
                    MatchStatus.MATCHED
                    if candidate_evidence is not None
                    else MatchStatus.NOT_ENOUGH_INFORMATION
                ),
                job_evidence=job_evidence,
                candidate_evidence=candidate_evidence,
                is_application_blocker=(
                    requirement.is_application_blocker
                ),
            )
        )

    return requirement_matches

def extract_skill_evidence(
    text: str,
    skill: str,
) -> str | None:
    for raw_line in text.splitlines():
        line = raw_line.strip()

        if line and contains_skill(line, skill):
            return line

    return None

def extract_requirement_evidence(
    text: str,
    requirement: RequirementDefinition,
) -> str | None:
    search_terms = (
        requirement.name,
        *requirement.aliases,
    )

    for search_term in search_terms:
        evidence = extract_skill_evidence(
            text,
            search_term,
        )

        if evidence is not None:
            return evidence

    return None

def extract_requirement_evidence(
    text: str,
    requirement: RequirementDefinition,
) -> str | None:
    search_terms = (
        requirement.name,
        *requirement.aliases,
    )

    for search_term in search_terms:
        evidence = extract_skill_evidence(
            text,
            search_term,
        )

        if evidence is not None:
            return evidence

    return None
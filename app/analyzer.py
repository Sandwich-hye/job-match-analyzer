import re

from collections.abc import Sequence
from app.models import (
    MatchResult,
    MatchStatus,
    RequirementCategory,
    RequirementMatch,
)

from app.scoring import (
    calculate_category_scores,
    calculate_requirement_score,
    calculate_weighted_score,
)

def contains_skill(text: str, skill: str) -> bool:
    escaped_skill = re.escape(skill)

    pattern = rf"(?<!\w){escaped_skill}(?!\w)"

    return re.search(
        pattern,
        text,
        flags=re.IGNORECASE,
    ) is not None

def find_matching_skills(
    job_description: str,
    resume: str,
    skills: Sequence[str]
) -> tuple[list[str], list[str]]:
    required_skills = [
        skill
        for skill in skills
        if contains_skill(job_description, skill)
    ]

    matched_skills = [
        skill
        for skill in required_skills
        if contains_skill(resume, skill)
    ]

    missing_skills = [
        skill
        for skill in required_skills
        if not contains_skill(resume, skill)
    ]

    return matched_skills, missing_skills


def analyse_job_match(
    job_description: str,
    resume: str,
    skills: Sequence[str],
) -> MatchResult:
    matched_skills, missing_skills = find_matching_skills(
        job_description,
        resume,
        skills,
    )

    requirement_matches = build_requirement_matches(
        job_description,
        resume,
        skills,
    )

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
    skills: Sequence[str],
) -> list[RequirementMatch]:
    requirement_matches: list[RequirementMatch] = []

    for skill in skills:
        job_evidence = extract_skill_evidence(
            job_description,
            skill,
        )

        if job_evidence is None:
            continue

        candidate_evidence = extract_skill_evidence(
            resume,
            skill,
        )

        requirement_matches.append(
            RequirementMatch(
                requirement=skill,
                category=RequirementCategory.CORE_SKILL,
                status=(
                    MatchStatus.MATCHED
                    if candidate_evidence is not None
                    else MatchStatus.NOT_ENOUGH_INFORMATION
                ),
                job_evidence=job_evidence,
                candidate_evidence=candidate_evidence,
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
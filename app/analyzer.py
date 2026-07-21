import re

from collections.abc import Sequence
from app.models import MatchResult, MatchStatus, RequirementMatch

def contains_skill(text: str, skill: str) -> bool:
    escaped_skill = re.escape(skill)

    pattern = rf"(?<!\w){escaped_skill}(?!\w)"

    return re.search(
        pattern,
        text,
        flags=re.IGNORECASE,
    ) is not None


def calculate_match_score(
    matched_skills: list[str],
    missing_skills: list[str],
) -> float:
    total_required_skills = len(matched_skills) + len(missing_skills)

    if total_required_skills == 0:
        return 0.0

    score = len(matched_skills) / total_required_skills * 100

    return round(score, 2)


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

    match_score = calculate_match_score(
        matched_skills,
        missing_skills,
    )

    return MatchResult(
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        match_score=match_score,
        requirement_matches=requirement_matches,
    )

def build_requirement_matches(
    job_description: str,
    resume: str,
    skills: Sequence[str],
) -> list[RequirementMatch]:
    requirement_matches: list[RequirementMatch] = []

    for skill in skills:
        if not contains_skill(job_description, skill):
            continue

        has_resume_evidence = contains_skill(resume, skill)

        requirement_matches.append(
            RequirementMatch(
                requirement=skill,
                status=(
                    MatchStatus.MATCHED
                    if has_resume_evidence
                    else MatchStatus.NOT_ENOUGH_INFORMATION
                ),
                candidate_evidence=(
                    skill
                    if has_resume_evidence
                    else None
                ),
            )
        )

    return requirement_matches
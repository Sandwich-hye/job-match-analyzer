import re

from app.models import MatchResult


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
    skills: list[str],
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
    skills: list[str],
) -> MatchResult:
    matched_skills, missing_skills = find_matching_skills(
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
    )
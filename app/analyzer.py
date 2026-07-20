def find_matching_skills(
    job_description: str,
    resume: str,
    skills: list[str],
) -> tuple[list[str], list[str]]:
    job_description_lower = job_description.lower()
    resume_lower = resume.lower()

    required_skills = [
        skill
        for skill in skills
        if skill.lower() in job_description_lower
    ]

    matched_skills = [
        skill
        for skill in required_skills
        if skill.lower() in resume_lower
    ]

    missing_skills = [
        skill
        for skill in required_skills
        if skill.lower() not in resume_lower
    ]

    return matched_skills, missing_skills

def calculate_match_score(
    matched_skills: list[str],
    missing_skills: list[str],
) -> float:
    total_required_skills = len(matched_skills) + len(missing_skills)

    if total_required_skills == 0:
        return 0.0

    score = len(matched_skills) / total_required_skills * 100

    return round(score, 2)
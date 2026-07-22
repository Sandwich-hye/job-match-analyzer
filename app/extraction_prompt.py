import json

from app.extraction_models import JobExtraction


JOB_EXTRACTION_SYSTEM_PROMPT = """
You are a job description extraction assistant.

Extract factual information only from the supplied job description.

Rules:
1. Do not invent information that is not present.
2. Use exact evidence copied from the job description.
3. Return only valid JSON.
4. Do not include Markdown code fences.
5. Do not include explanations before or after the JSON.
6. Use "unknown" when the work mode cannot be determined.

Requirement names:
7. Use concise, normalized requirement names such as
   "Python", "SQL", "AWS", "Backend development experience",
   or "New Zealand work rights".
8. Do not include wording such as "strong", "required",
   "preferred", "desirable", "nice to have", or
   "experience with" in a normalized requirement name.
9. Preserve the full original wording in job_evidence.

Category and importance:
10. Determine category and importance independently.
11. Category describes what kind of requirement it is.
12. Importance describes whether the requirement is mandatory
    or optional.
13. Do not choose a category only because the sentence contains
    a word such as "experience", "required", or "preferred".

Category rules:
14. Use "core_skill" for programming languages, frameworks,
    databases, cloud platforms, development tools, technical
    methods, and named technical skills.
15. Examples of "core_skill" include Python, SQL, AWS, Docker,
    React, FastAPI, Git, PostgreSQL, and machine learning.
16. A technical skill remains "core_skill" whether it is
    required or preferred.
17. Use "experience" for duration, seniority, scale, or depth
    of previous work, such as "3+ years of backend development"
    or "experience leading engineering teams".
18. Do not classify "Experience with Python" or
    "Experience with SQL" as "experience". These are named
    technical skills and must use "core_skill".
19. Use "responsibility" for work the employee will be expected
    to perform, such as designing systems, mentoring developers,
    managing stakeholders, or maintaining production services.
20. Use "feasibility" for eligibility or practical constraints,
    such as work rights, citizenship, residency, mandatory
    licences, mandatory certifications, security clearance,
    location, or required travel.
21. Use "bonus" only for an explicitly stated additional
    advantage that does not meaningfully fit "core_skill",
    "experience", "responsibility", or "feasibility".
22. Do not use "bonus" merely because a requirement is preferred,
    desirable, beneficial, optional, or nice to have.

Importance rules:
23. Use importance="required" when the job description presents
    the requirement as mandatory, essential, minimum, necessary,
    or required.
24. Use importance="preferred" when the job description presents
    the requirement as preferred, desirable, beneficial,
    advantageous, ideal, optional, or nice to have.
25. When the wording does not clearly indicate that a requirement
    is optional, use importance="required" only when the job
    description clearly treats it as an expected requirement.

Application blockers:
26. A required skill, experience requirement, or responsibility
    is not automatically an application blocker.
27. Set is_application_blocker=true only for an explicit
    eligibility condition that could prevent the candidate from
    applying or legally performing the role.
28. Examples include mandatory work rights, citizenship,
    residency, professional licences, security clearance,
    or legally required certification.
29. Every application blocker must use category="feasibility".
30. A feasibility requirement is an application blocker only
    when the job description clearly states that it is mandatory.

Classification examples:
31. "Python is required" means:
    category="core_skill",
    importance="required",
    is_application_blocker=false.

32. "Experience with SQL is required" means:
    category="core_skill",
    importance="required",
    is_application_blocker=false.

33. "AWS experience is preferred" means:
    category="core_skill",
    importance="preferred",
    is_application_blocker=false.

34. "3+ years of backend development experience is required"
    means:
    category="experience",
    importance="required",
    is_application_blocker=false.

35. "You will mentor junior developers" means:
    category="responsibility",
    importance="required",
    is_application_blocker=false.

36. "Applicants must have the legal right to work in
    New Zealand" means:
    category="feasibility",
    importance="required",
    is_application_blocker=true.
""".strip()


def build_job_extraction_prompt(
    job_description: str,
) -> str:
    cleaned_job_description = job_description.strip()

    if not cleaned_job_description:
        raise ValueError(
            "job description must not be empty"
        )

    json_schema = json.dumps(
        JobExtraction.model_json_schema(),
        indent=2,
    )

    return f"""
Extract the job information from the job description below.

Return a JSON object that conforms exactly to this JSON schema:

{json_schema}

Job description:

{cleaned_job_description}
""".strip()
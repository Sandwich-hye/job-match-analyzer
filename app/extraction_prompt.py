import json

from app.extraction_models import JobExtraction


JOB_EXTRACTION_SYSTEM_PROMPT = """
You are a job description extraction assistant.

Extract factual information only from the supplied job description.

Rules:
1. Do not invent information that is not present.
2. Use the exact evidence from the job description.
3. Return only valid JSON.
4. Do not include Markdown code fences.
5. Do not include explanations before or after the JSON.
6. Use "unknown" when the work mode cannot be determined.
7. Mark a requirement as an application blocker only when the
   job description clearly states that it is mandatory for applying.
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
from app.extraction_models import JobExtraction
from app.extraction_parser import parse_job_extraction
from app.extraction_prompt import (
    JOB_EXTRACTION_SYSTEM_PROMPT,
    build_job_extraction_prompt,
)
from app.llm_client import LLMClient


def extract_job_information(
    job_description: str,
    client: LLMClient,
) -> JobExtraction:
    user_prompt = build_job_extraction_prompt(
        job_description
    )

    raw_output = client.generate(
        system_prompt=JOB_EXTRACTION_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        response_schema=(
            JobExtraction.model_json_schema()
        ),
    )

    return parse_job_extraction(raw_output)
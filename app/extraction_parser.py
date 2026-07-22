from app.extraction_models import JobExtraction


def parse_job_extraction(
    raw_output: str,
) -> JobExtraction:
    if not raw_output.strip():
        raise ValueError(
            "LLM output must not be empty"
        )

    return JobExtraction.model_validate_json(
        raw_output
    )
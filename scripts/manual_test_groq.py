from app.groq_client import GroqLLMClient
from app.job_extraction_service import (
    extract_job_information,
)
from app.settings import load_groq_settings


TEST_JOB_DESCRIPTION = """
Software Engineer

Location: Auckland, New Zealand
Work arrangement: Hybrid

Requirements:
- Strong Python development experience is required.
- Experience with SQL is required.
- AWS experience is preferred.
- Applicants must have the legal right to work in New Zealand.
""".strip()


def main() -> None:
    settings = load_groq_settings()

    client = GroqLLMClient(
        settings=settings,
    )

    result = extract_job_information(
        job_description=TEST_JOB_DESCRIPTION,
        client=client,
    )

    print("=" * 50)
    print("Groq job extraction result")
    print("=" * 50)
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
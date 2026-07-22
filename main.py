import argparse

from pathlib import Path
from app.skills import KNOWN_SKILLS
from app.analyzer import analyse_job_match
from app.loaders import load_text_file
from collections.abc import Sequence

BASE_DIR = Path(__file__).resolve().parent

DEFAULT_JOB_DESCRIPTION_PATH = (
    BASE_DIR / "data" / "jd" / "software_engineer.txt"
)

DEFAULT_RESUME_PATH = (
    BASE_DIR / "data" / "resume" / "sample_resume.txt"
)

def parse_arguments(
    args: Sequence[str] | None = None,
) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Compare a job description with a resume "
            "and generate a structured match analysis."
        )
    )

    parser.add_argument(
        "--job-description",
        type=Path,
        default=DEFAULT_JOB_DESCRIPTION_PATH,
        help="Path to the job description text file.",
    )

    parser.add_argument(
        "--resume",
        type=Path,
        default=DEFAULT_RESUME_PATH,
        help="Path to the resume text file.",
    )

    return parser.parse_args(args)

def print_banner() -> None:
    print("=" * 50)
    print("Job Match Analyzer")
    print("AI-powered career matching system")
    print("=" * 50)


def main() -> None:
    print_banner()

    arguments = parse_arguments()

    job_description_path = arguments.job_description
    resume_path = arguments.resume

    print(f"\nJob description: {job_description_path}")
    print(f"Resume: {resume_path}")

    try:
        job_description = load_text_file(job_description_path)
        resume = load_text_file(resume_path)
    except (FileNotFoundError, ValueError) as error:
        print(f"Error: {error}")
        return

    print("\nJob description loaded successfully.")
    print("Resume loaded successfully.")

    result = analyse_job_match(
        job_description,
        resume,
        KNOWN_SKILLS,
    )

    print(f"\nOverall match score: {result.match_score}%")
    print(f"Requirement score: {result.requirement_score}%")
    print("\nMatching skills:")
    if result.matched_skills:
        for skill in result.matched_skills:
            print(f"- {skill}")
    else:
        print("- None")

    print("\nMissing skills:")
    if result.missing_skills:
        for skill in result.missing_skills:
            print(f"- {skill}")
    else:
        print("- None")
    
    output_path = Path("analysis_result.json")

    output_path.write_text(
        result.model_dump_json(indent=2),
        encoding="utf-8",
    )

    print(f"\nAnalysis saved to: {output_path.resolve()}")


if __name__ == "__main__":
    main()
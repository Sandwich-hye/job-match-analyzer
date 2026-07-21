from pathlib import Path

from app.analyzer import analyse_job_match
from app.loaders import load_text_file

def print_banner() -> None:
    print("=" * 50)
    print("Job Match Analyzer")
    print("AI-powered career matching system")
    print("=" * 50)


def main() -> None:
    print_banner()

    job_description_path_input = input(
        "Enter the path to the job description file: "
    )
    resume_path_input = input(
        "Enter the path to the resume file: "
    )

    job_description_path = Path(job_description_path_input)
    resume_path = Path(resume_path_input)

    try:
        job_description = load_text_file(job_description_path)
        resume = load_text_file(resume_path)
    except (FileNotFoundError, ValueError) as error:
        print(f"Error: {error}")
        return

    print("\nJob description loaded successfully.")
    print("Resume loaded successfully.")

    known_skills = [
        "Python",
        "SQL",
        "Git",
        "Docker",
        "React",
        "TypeScript",
        "FastAPI",
        "PostgreSQL",
        "AWS",
    ]

    result = analyse_job_match(
        job_description,
        resume,
        known_skills,
    )

    print(f"\nMatch score: {result.match_score}%")
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
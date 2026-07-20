from pathlib import Path

from app.loaders import load_job_description


def print_banner() -> None:
    """Display the application banner."""

    print("=" * 60)
    print("Job Match Analyzer")
    print("AI-powered Career Matching System")
    print("=" * 60)


def main() -> None:
    print_banner()

    path_input = input(
        "Enter the path to the job description file:\n> "
    ).strip()

    jd_path = Path(path_input)

    try:
        job_description = load_job_description(jd_path)
    except (FileNotFoundError, ValueError) as error:
        print(f"\nError: {error}")
        return

    print("\nJob description loaded successfully.")
    print("-" * 60)
    print(job_description)
    print("-" * 60)


if __name__ == "__main__":
    main()
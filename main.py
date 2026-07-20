from pathlib import Path


def load_job_description(path: Path) -> str:
    """Read a job description from a text file."""

    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def main():
    print("=" * 50)
    print("Job Match Analyzer")
    print("=" * 50)

    jd_path = Path("data/jd/software_engineer.txt")

    job_description = load_job_description(jd_path)

    print(job_description)


if __name__ == "__main__":
    main()
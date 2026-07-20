from pathlib import Path


def load_job_description(path: Path) -> str:
    """Load and validate a job description from a text file."""

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    if not path.is_file():
        raise ValueError(f"The provided path is not a file: {path}")

    if path.suffix.lower() != ".txt":
        raise ValueError("Only .txt files are currently supported.")

    job_description = path.read_text(encoding="utf-8")

    if not job_description.strip():
        raise ValueError("The job description file is empty.")

    return job_description
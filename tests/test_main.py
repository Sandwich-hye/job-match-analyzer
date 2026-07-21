from pathlib import Path

from main import (
    DEFAULT_JOB_DESCRIPTION_PATH,
    DEFAULT_RESUME_PATH,
    parse_arguments,
)


def test_parse_arguments_uses_default_file_paths() -> None:
    arguments = parse_arguments([])

    assert (
        arguments.job_description
        == DEFAULT_JOB_DESCRIPTION_PATH
    )
    assert arguments.resume == DEFAULT_RESUME_PATH


def test_parse_arguments_accepts_custom_file_paths() -> None:
    arguments = parse_arguments(
        [
            "--job-description",
            "data/jd/custom_job.txt",
            "--resume",
            "data/resume/custom_resume.txt",
        ]
    )

    assert arguments.job_description == Path(
        "data/jd/custom_job.txt"
    )
    assert arguments.resume == Path(
        "data/resume/custom_resume.txt"
    )
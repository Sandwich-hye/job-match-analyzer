from pathlib import Path

import pytest

from app.loaders import load_job_description


def test_load_job_description_returns_file_content(tmp_path: Path) -> None:
    jd_file = tmp_path / "job_description.txt"
    jd_file.write_text(
        "Python Developer\n\nRequirements:\n- Python\n- SQL",
        encoding="utf-8",
    )

    result = load_job_description(jd_file)

    assert result == "Python Developer\n\nRequirements:\n- Python\n- SQL"


def test_load_job_description_raises_error_when_file_does_not_exist(
    tmp_path: Path,
) -> None:
    missing_file = tmp_path / "missing.txt"

    with pytest.raises(FileNotFoundError, match="File not found"):
        load_job_description(missing_file)


def test_load_job_description_raises_error_for_unsupported_file_type(
    tmp_path: Path,
) -> None:
    pdf_file = tmp_path / "job_description.pdf"
    pdf_file.write_text("Example content", encoding="utf-8")

    with pytest.raises(
        ValueError,
        match=r"Only \.txt files are currently supported",
    ):
        load_job_description(pdf_file)


def test_load_job_description_raises_error_for_empty_file(
    tmp_path: Path,
) -> None:
    empty_file = tmp_path / "empty.txt"
    empty_file.write_text("   \n", encoding="utf-8")

    with pytest.raises(
        ValueError,
        match="The job description file is empty",
    ):
        load_job_description(empty_file)

def test_load_job_description_raises_error_when_path_is_directory(
    tmp_path: Path,
) -> None:
    directory = tmp_path / "job_descriptions"
    directory.mkdir()

    with pytest.raises(
        ValueError,
        match="The provided path is not a file",
    ):
        load_job_description(directory)
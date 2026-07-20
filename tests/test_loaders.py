from pathlib import Path

import pytest

from app.loaders import load_text_file


def test_load_text_file_returns_file_content(tmp_path: Path) -> None:
    text_file = tmp_path / "job_description.txt"
    expected_content = "Python Developer\n\nRequirements:\n- Python\n- SQL"

    text_file.write_text(expected_content, encoding="utf-8")

    result = load_text_file(text_file)

    assert result == expected_content


def test_load_text_file_raises_error_when_file_does_not_exist(
    tmp_path: Path,
) -> None:
    missing_file = tmp_path / "missing.txt"

    with pytest.raises(FileNotFoundError, match="File not found"):
        load_text_file(missing_file)


def test_load_text_file_raises_error_for_unsupported_file_type(
    tmp_path: Path,
) -> None:
    pdf_file = tmp_path / "document.pdf"
    pdf_file.write_text("Example content", encoding="utf-8")

    with pytest.raises(
        ValueError,
        match=r"Only \.txt files are currently supported",
    ):
        load_text_file(pdf_file)


def test_load_text_file_raises_error_for_empty_file(
    tmp_path: Path,
) -> None:
    empty_file = tmp_path / "empty.txt"
    empty_file.write_text("   \n", encoding="utf-8")

    with pytest.raises(
        ValueError,
        match="The file is empty",
    ):
        load_text_file(empty_file)


def test_load_text_file_raises_error_when_path_is_directory(
    tmp_path: Path,
) -> None:
    directory = tmp_path / "documents"
    directory.mkdir()

    with pytest.raises(
        ValueError,
        match="The provided path is not a file",
    ):
        load_text_file(directory)
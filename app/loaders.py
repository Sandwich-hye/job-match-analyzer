from pathlib import Path


def load_text_file(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    if not path.is_file():
        raise ValueError("The provided path is not a file.")

    if path.suffix.lower() != ".txt":
        raise ValueError("Only .txt files are currently supported.")

    content = path.read_text(encoding="utf-8")

    if not content.strip():
        raise ValueError("The file is empty.")

    return content
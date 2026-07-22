import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_ENV_FILE = BASE_DIR / ".env"


@dataclass(frozen=True, slots=True)
class GroqSettings:
    api_key: str
    model: str


def load_groq_settings(
    env_file: Path | None = DEFAULT_ENV_FILE,
) -> GroqSettings:
    if env_file is not None:
        load_dotenv(
            dotenv_path=env_file,
            override=False,
        )

    api_key = os.getenv(
        "GROQ_API_KEY",
        "",
    ).strip()

    model = os.getenv(
        "GROQ_MODEL",
        "",
    ).strip()

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is not set"
        )

    if not model:
        raise ValueError(
            "GROQ_MODEL is not set"
        )

    return GroqSettings(
        api_key=api_key,
        model=model,
    )
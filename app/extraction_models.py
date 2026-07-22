from enum import StrEnum
from typing import Self

from pydantic import (
    BaseModel,
    Field,
    field_validator,
    model_validator,
)

from app.models import RequirementCategory


class RequirementImportance(StrEnum):
    REQUIRED = "required"
    PREFERRED = "preferred"


class WorkMode(StrEnum):
    ONSITE = "onsite"
    HYBRID = "hybrid"
    REMOTE = "remote"
    UNKNOWN = "unknown"


class ExtractedRequirement(BaseModel):
    requirement: str = Field(min_length=1)
    category: RequirementCategory
    importance: RequirementImportance
    job_evidence: str = Field(min_length=1)
    is_application_blocker: bool = False

    @field_validator(
        "requirement",
        "job_evidence",
    )
    @classmethod
    def strip_required_text(
        cls,
        value: str,
    ) -> str:
        stripped_value = value.strip()

        if not stripped_value:
            raise ValueError(
                "text must not be empty"
            )

        return stripped_value


class JobExtraction(BaseModel):
    job_title: str | None = None
    location: str | None = None
    work_mode: WorkMode = WorkMode.UNKNOWN

    requirements: list[ExtractedRequirement] = Field(
        default_factory=list,
    )

    @field_validator(
        "job_title",
        "location",
    )
    @classmethod
    def normalize_optional_text(
        cls,
        value: str | None,
    ) -> str | None:
        if value is None:
            return None

        stripped_value = value.strip()

        return stripped_value or None

    @model_validator(mode="after")
    def validate_unique_requirements(
        self,
    ) -> Self:
        normalized_names = [
            requirement.requirement.casefold()
            for requirement in self.requirements
        ]

        if len(normalized_names) != len(
            set(normalized_names)
        ):
            raise ValueError(
                "requirements must have unique names"
            )

        return self
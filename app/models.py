from enum import StrEnum

from pydantic import BaseModel, Field


class MatchStatus(StrEnum):
    MATCHED = "matched"
    PARTIALLY_MATCHED = "partially_matched"
    NOT_MATCHED = "not_matched"
    NOT_ENOUGH_INFORMATION = "not_enough_information"


class RequirementMatch(BaseModel):
    requirement: str
    status: MatchStatus
    candidate_evidence: str | None = None
    is_application_blocker: bool = False


class MatchResult(BaseModel):
    matched_skills: list[str]
    missing_skills: list[str]
    match_score: float = Field(ge=0, le=100)
from enum import StrEnum

from pydantic import BaseModel, Field


class MatchStatus(StrEnum):
    MATCHED = "matched"
    PARTIALLY_MATCHED = "partially_matched"
    NOT_MATCHED = "not_matched"
    NOT_ENOUGH_INFORMATION = "not_enough_information"

class Recommendation(StrEnum):
    APPLY = "apply"
    CONSIDER = "consider"
    SKIP = "skip"

class RequirementCategory(StrEnum):
    CORE_SKILL = "core_skill"
    EXPERIENCE = "experience"
    RESPONSIBILITY = "responsibility"
    BONUS = "bonus"
    FEASIBILITY = "feasibility"

class RequirementImportance(StrEnum):
    REQUIRED = "required"
    PREFERRED = "preferred"

class RequirementMatch(BaseModel):
    requirement: str
    category: RequirementCategory
    importance: RequirementImportance = (
        RequirementImportance.REQUIRED
    )
    status: MatchStatus
    job_evidence: str
    candidate_evidence: str | None = None
    is_application_blocker: bool = False

class MatchResult(BaseModel):
    matched_skills: list[str]
    missing_skills: list[str]
    requirement_score: float = Field(ge=0, le=100)
    match_score: float = Field(ge=0, le=100)
    recommendation: Recommendation
    category_scores: dict[RequirementCategory, float] = Field(
        default_factory=dict,
    )
    requirement_matches: list[RequirementMatch] = Field(
        default_factory=list,
    )
    potential_application_blockers: list[str] = Field(
        default_factory=list,
    )
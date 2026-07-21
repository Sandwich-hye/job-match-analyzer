from pydantic import BaseModel, Field


class MatchResult(BaseModel):
    matched_skills: list[str]
    missing_skills: list[str]
    match_score: float = Field(ge=0, le=100)
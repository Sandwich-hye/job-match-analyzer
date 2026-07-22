from dataclasses import dataclass

from app.models import RequirementCategory


@dataclass(frozen=True, slots=True)
class RequirementDefinition:
    name: str
    category: RequirementCategory
    aliases: tuple[str, ...] = ()
    is_application_blocker: bool = False


KNOWN_REQUIREMENTS: tuple[RequirementDefinition, ...] = (
    RequirementDefinition(
        name="Python",
        category=RequirementCategory.CORE_SKILL,
    ),
    RequirementDefinition(
        name="SQL",
        category=RequirementCategory.CORE_SKILL,
    ),
    RequirementDefinition(
        name="Git",
        category=RequirementCategory.CORE_SKILL,
    ),
    RequirementDefinition(
        name="Docker",
        category=RequirementCategory.CORE_SKILL,
    ),
    RequirementDefinition(
        name="React",
        category=RequirementCategory.CORE_SKILL,
    ),
    RequirementDefinition(
        name="TypeScript",
        category=RequirementCategory.CORE_SKILL,
        aliases=("TS",),
    ),
    RequirementDefinition(
        name="FastAPI",
        category=RequirementCategory.CORE_SKILL,
    ),
    RequirementDefinition(
        name="PostgreSQL",
        category=RequirementCategory.CORE_SKILL,
        aliases=(
            "Postgres",
            "Postgre SQL",
        ),
    ),
    RequirementDefinition(
        name="AWS",
        category=RequirementCategory.CORE_SKILL,
        aliases=("Amazon Web Services",),
    ),
)
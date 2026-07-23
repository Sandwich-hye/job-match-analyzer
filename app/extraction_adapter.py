from app.analyzer import extract_requirement_evidence
from app.extraction_models import (
    ExtractedRequirement,
    JobExtraction,
)
from app.models import (
    MatchStatus,
    RequirementMatch,
)
from app.skills import (
    KNOWN_REQUIREMENTS,
    RequirementDefinition,
)


def _normalize_requirement_name(
    value: str,
) -> str:
    return " ".join(
        value.casefold().split()
    )


def _find_catalog_requirement(
    name: str,
) -> RequirementDefinition | None:
    normalized_name = _normalize_requirement_name(
        name
    )

    for requirement in KNOWN_REQUIREMENTS:
        possible_names = (
            requirement.name,
            *requirement.aliases,
        )

        if any(
            _normalize_requirement_name(
                possible_name
            )
            == normalized_name
            for possible_name in possible_names
        ):
            return requirement

    return None


def adapt_extracted_requirement(
    extracted: ExtractedRequirement,
) -> RequirementDefinition:
    catalog_requirement = (
        _find_catalog_requirement(
            extracted.requirement
        )
    )

    if catalog_requirement is None:
        name = extracted.requirement
        aliases: tuple[str, ...] = ()
    else:
        name = catalog_requirement.name
        aliases = catalog_requirement.aliases

    return RequirementDefinition(
        name=name,
        category=extracted.category,
        importance=extracted.importance,
        aliases=aliases,
        is_application_blocker=(
            extracted.is_application_blocker
        ),
    )


def build_requirement_matches_from_extraction(
    extraction: JobExtraction,
    resume: str,
) -> list[RequirementMatch]:
    matches: list[RequirementMatch] = []

    for extracted in extraction.requirements:
        requirement = (
            adapt_extracted_requirement(
                extracted
            )
        )

        candidate_evidence = (
            extract_requirement_evidence(
                resume,
                requirement,
            )
        )

        status = (
            MatchStatus.MATCHED
            if candidate_evidence is not None
            else MatchStatus.NOT_MATCHED
        )

        matches.append(
            RequirementMatch(
                requirement=requirement.name,
                category=requirement.category,
                importance=requirement.importance,
                status=status,
                job_evidence=(
                    extracted.job_evidence
                ),
                candidate_evidence=(
                    candidate_evidence
                ),
                is_application_blocker=(
                    requirement
                    .is_application_blocker
                ),
            )
        )

    return matches
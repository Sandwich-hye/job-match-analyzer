from app.skills import KNOWN_REQUIREMENTS

def test_requirement_catalog_has_unique_names() -> None:
    normalized_names = [
        requirement.name.casefold()
        for requirement in KNOWN_REQUIREMENTS
    ]

    assert len(normalized_names) == len(
        set(normalized_names)
    )


def test_aws_requirement_contains_full_name_alias() -> None:
    aws_requirement = next(
        requirement
        for requirement in KNOWN_REQUIREMENTS
        if requirement.name == "AWS"
    )

    assert "Amazon Web Services" in aws_requirement.aliases

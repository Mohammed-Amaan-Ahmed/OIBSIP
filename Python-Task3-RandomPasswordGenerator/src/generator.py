"""Secure password generation logic."""

import secrets
import string
from typing import Dict


CHARACTER_SETS: Dict[str, str] = {
    "uppercase": string.ascii_uppercase,
    "lowercase": string.ascii_lowercase,
    "numbers": string.digits,
    "symbols": string.punctuation,
}

AMBIGUOUS_CHARACTERS = set("0Oo1Il")


class PasswordGenerationError(ValueError):
    """Raised when password generation parameters are invalid."""


def validate_length(length: int) -> int:
    """Validate and return a password length.

    Passwords must contain at least 8 characters.
    """
    try:
        value = int(length)
    except (TypeError, ValueError) as exc:
        raise PasswordGenerationError(
            "Password length must be a whole number."
        ) from exc

    if value < 8:
        raise PasswordGenerationError(
            "Password length must be at least 8 characters."
        )

    return value


def validate_categories(categories: Dict[str, bool]) -> None:
    """Validate the selected password character categories."""
    selected = [
        name
        for name in CHARACTER_SETS
        if categories.get(name, False)
    ]

    if len(selected) < 2:
        raise PasswordGenerationError(
            "Select at least two character categories."
        )


def _build_character_sets(
    categories: Dict[str, bool],
    exclude_ambiguous: bool,
) -> Dict[str, str]:
    """Build the selected character sets."""
    selected_sets = {}

    for name, characters in CHARACTER_SETS.items():
        if not categories.get(name, False):
            continue

        if exclude_ambiguous:
            characters = "".join(
                character
                for character in characters
                if character not in AMBIGUOUS_CHARACTERS
            )

        if not characters:
            raise PasswordGenerationError(
                f"No usable characters remain for {name}."
            )

        selected_sets[name] = characters

    return selected_sets


def generate_password(
    length: int,
    categories: Dict[str, bool],
    exclude_ambiguous: bool = False,
) -> str:
    """Generate a cryptographically secure password.

    Every selected category is guaranteed to contribute at least
    one character. Remaining characters are selected from the
    combined character pool and securely shuffled.

    Passwords are returned only in memory and are never persisted.
    """
    password_length = validate_length(length)
    validate_categories(categories)

    selected_sets = _build_character_sets(
        categories,
        exclude_ambiguous,
    )

    if password_length < len(selected_sets):
        raise PasswordGenerationError(
            "Password length is too short for the selected categories."
        )

    guaranteed_characters = [
        secrets.choice(characters)
        for characters in selected_sets.values()
    ]

    combined_pool = "".join(selected_sets.values())

    remaining_characters = [
        secrets.choice(combined_pool)
        for _ in range(
            password_length - len(guaranteed_characters)
        )
    ]

    password_characters = (
        guaranteed_characters + remaining_characters
    )

    secrets.SystemRandom().shuffle(password_characters)

    return "".join(password_characters)
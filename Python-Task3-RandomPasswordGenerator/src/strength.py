"""Password strength analysis logic."""

import math
import string
from typing import Tuple


def calculate_entropy(password: str) -> float:
    """Estimate password entropy in bits.

    The estimate is based on the size of the character pool
    represented by the password's character categories.
    """
    if not password:
        return 0.0

    pool_size = 0

    if any(character in string.ascii_lowercase for character in password):
        pool_size += 26

    if any(character in string.ascii_uppercase for character in password):
        pool_size += 26

    if any(character in string.digits for character in password):
        pool_size += 10

    if any(character in string.punctuation for character in password):
        pool_size += len(string.punctuation)

    if pool_size == 0:
        return 0.0

    return len(password) * math.log2(pool_size)


def assess_password_strength(password: str) -> Tuple[str, float]:
    """Return a strength label and estimated entropy.

    Strength levels:
        Weak: fewer than 40 bits
        Medium: 40 to under 70 bits
        Strong: 70 bits or more
    """
    entropy = calculate_entropy(password)

    if entropy < 40:
        strength = "Weak"
    elif entropy < 70:
        strength = "Medium"
    else:
        strength = "Strong"

    return strength, round(entropy, 2)
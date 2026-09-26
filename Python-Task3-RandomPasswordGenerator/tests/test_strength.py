"""Tests for password strength analysis."""

import unittest

from src.strength import (
    assess_password_strength,
    calculate_entropy,
)


class TestCalculateEntropy(unittest.TestCase):
    """Test entropy estimation."""

    def test_empty_password_has_zero_entropy(self):
        self.assertEqual(calculate_entropy(""), 0.0)

    def test_lowercase_password_has_positive_entropy(self):
        entropy = calculate_entropy("abcdefgh")

        self.assertGreater(entropy, 0)

    def test_mixed_character_password_has_higher_entropy(self):
        lowercase_entropy = calculate_entropy("abcdefgh")
        mixed_entropy = calculate_entropy("Abcd1234!")

        self.assertGreater(mixed_entropy, lowercase_entropy)


class TestPasswordStrength(unittest.TestCase):
    """Test strength classification."""

    def test_short_lowercase_password_is_weak(self):
        strength, entropy = assess_password_strength("abc")

        self.assertEqual(strength, "Weak")
        self.assertGreaterEqual(entropy, 0)

    def test_medium_password(self):
        strength, entropy = assess_password_strength(
            "Abcd1234"
        )

        self.assertEqual(strength, "Medium")
        self.assertGreaterEqual(entropy, 40)
        self.assertLess(entropy, 70)

    def test_strong_password(self):
        strength, entropy = assess_password_strength(
            "Abcd1234!@#$5678"
        )

        self.assertEqual(strength, "Strong")
        self.assertGreaterEqual(entropy, 70)


if __name__ == "__main__":
    unittest.main()
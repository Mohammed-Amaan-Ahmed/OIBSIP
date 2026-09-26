"""Tests for the secure password generator."""

import string
import unittest

from src.generator import (
    PasswordGenerationError,
    generate_password,
    validate_categories,
    validate_length,
)


class TestValidateLength(unittest.TestCase):
    """Test password length validation."""

    def test_valid_length(self):
        self.assertEqual(validate_length(12), 12)

    def test_minimum_length(self):
        self.assertEqual(validate_length(8), 8)

    def test_length_below_minimum(self):
        with self.assertRaises(PasswordGenerationError):
            validate_length(7)

    def test_non_numeric_length(self):
        with self.assertRaises(PasswordGenerationError):
            validate_length("abc")


class TestValidateCategories(unittest.TestCase):
    """Test character-category validation."""

    def test_two_categories_are_valid(self):
        categories = {
            "uppercase": True,
            "lowercase": True,
            "numbers": False,
            "symbols": False,
        }

        validate_categories(categories)

    def test_one_category_is_rejected(self):
        categories = {
            "uppercase": True,
            "lowercase": False,
            "numbers": False,
            "symbols": False,
        }

        with self.assertRaises(PasswordGenerationError):
            validate_categories(categories)


class TestGeneratePassword(unittest.TestCase):
    """Test password generation behavior."""

    def setUp(self):
        self.all_categories = {
            "uppercase": True,
            "lowercase": True,
            "numbers": True,
            "symbols": True,
        }

    def test_password_has_requested_length(self):
        password = generate_password(
            16,
            self.all_categories,
        )

        self.assertEqual(len(password), 16)

    def test_selected_categories_are_guaranteed(self):
        categories = {
            "uppercase": True,
            "lowercase": True,
            "numbers": True,
            "symbols": False,
        }

        password = generate_password(16, categories)

        self.assertTrue(any(c in string.ascii_uppercase for c in password))
        self.assertTrue(any(c in string.ascii_lowercase for c in password))
        self.assertTrue(any(c in string.digits for c in password))

    def test_symbols_are_generated_when_selected(self):
        categories = {
            "uppercase": True,
            "lowercase": False,
            "numbers": False,
            "symbols": True,
        }

        password = generate_password(12, categories)

        self.assertTrue(
            any(c in string.ascii_uppercase for c in password)
        )
        self.assertTrue(
            any(c in string.punctuation for c in password)
        )

    def test_excluded_ambiguous_characters_are_absent(self):
        password = generate_password(
            32,
            self.all_categories,
            exclude_ambiguous=True,
        )

        for character in password:
            self.assertNotIn(character, "0Oo1Il")

    def test_one_category_is_rejected(self):
        categories = {
            "uppercase": True,
            "lowercase": False,
            "numbers": False,
            "symbols": False,
        }

        with self.assertRaises(PasswordGenerationError):
            generate_password(12, categories)

    def test_short_password_is_rejected(self):
        with self.assertRaises(PasswordGenerationError):
            generate_password(7, self.all_categories)

    def test_repeated_generation_produces_passwords(self):
        passwords = {
            generate_password(20, self.all_categories)
            for _ in range(20)
        }

        self.assertGreater(len(passwords), 1)


if __name__ == "__main__":
    unittest.main()
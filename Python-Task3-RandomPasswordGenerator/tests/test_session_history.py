"""Tests for in-memory password session history."""

import unittest

from src.session_history import PasswordSessionHistory


class TestPasswordSessionHistory(unittest.TestCase):
    def test_history_stores_passwords(self):
        history = PasswordSessionHistory()

        history.add("Password1!")
        history.add("Password2!")

        self.assertEqual(
            history.get_recent(),
            ["Password2!", "Password1!"],
        )

    def test_history_keeps_only_last_five(self):
        history = PasswordSessionHistory()

        for number in range(1, 7):
            history.add(f"Password{number}!")

        self.assertEqual(len(history), 5)
        self.assertEqual(
            history.get_recent(),
            [
                "Password6!",
                "Password5!",
                "Password4!",
                "Password3!",
                "Password2!",
            ],
        )

    def test_empty_password_is_rejected(self):
        history = PasswordSessionHistory()

        with self.assertRaises(ValueError):
            history.add("")

    def test_clear_removes_session_history(self):
        history = PasswordSessionHistory()
        history.add("Password1!")

        history.clear()

        self.assertEqual(len(history), 0)
        self.assertEqual(history.get_recent(), [])

    def test_custom_history_size(self):
        history = PasswordSessionHistory(max_items=3)

        history.add("Password1!")
        history.add("Password2!")
        history.add("Password3!")
        history.add("Password4!")

        self.assertEqual(
            history.get_recent(),
            ["Password4!", "Password3!", "Password2!"],
        )


if __name__ == "__main__":
    unittest.main()
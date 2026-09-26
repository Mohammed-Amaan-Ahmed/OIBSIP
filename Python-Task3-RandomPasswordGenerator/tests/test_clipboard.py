"""Tests for clipboard utilities."""

import unittest
from unittest.mock import patch

from src.clipboard import copy_password


class TestCopyPassword(unittest.TestCase):
    @patch("src.clipboard.pyperclip.copy")
    def test_password_is_copied(self, mock_copy):
        password = "Abcd1234!"

        copy_password(password)

        mock_copy.assert_called_once_with(password)

    def test_empty_password_is_rejected(self):
        with self.assertRaises(ValueError):
            copy_password("")


if __name__ == "__main__":
    unittest.main()
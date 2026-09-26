"""Clipboard utilities for the password generator."""

import pyperclip


def copy_password(password: str) -> None:
    """Copy a password to the system clipboard."""
    if not password:
        raise ValueError("Password cannot be empty.")

    pyperclip.copy(password)

"""In-memory session history for generated passwords."""

from collections import deque


class PasswordSessionHistory:
    """Store only the most recent generated passwords in memory."""

    def __init__(self, max_items: int = 5):
        if max_items <= 0:
            raise ValueError("max_items must be greater than zero.")

        self._passwords = deque(maxlen=max_items)

    def add(self, password: str) -> None:
        """Add a password to the current session history."""
        if not password:
            raise ValueError("Password cannot be empty.")

        self._passwords.append(password)

    def get_recent(self) -> list[str]:
        """Return recent passwords from newest to oldest."""
        return list(reversed(self._passwords))

    def clear(self) -> None:
        """Clear the current session history."""
        self._passwords.clear()

    def __len__(self) -> int:
        """Return the number of passwords currently stored."""
        return len(self._passwords)
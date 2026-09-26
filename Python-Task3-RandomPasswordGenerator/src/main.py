"""Application entry point for the random password generator."""

from src.gui import create_application


def main() -> None:
    """Start the password generator application."""
    root, _application = create_application()
    root.mainloop()


if __name__ == "__main__":
    main()
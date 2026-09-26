"""Application entry point for the BMI Calculator."""

from .gui import create_application


def main() -> None:
    """Start the BMI Calculator application."""
    root = create_application()
    root.mainloop()


if __name__ == "__main__":
    main()
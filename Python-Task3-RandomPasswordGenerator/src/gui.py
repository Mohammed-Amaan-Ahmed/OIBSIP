"""Tkinter GUI for the advanced random password generator."""

import tkinter as tk
from tkinter import messagebox, ttk

from src.clipboard import copy_password
from src.generator import PasswordGenerationError, generate_password
from src.session_history import PasswordSessionHistory
from src.strength import assess_password_strength


class PasswordGeneratorGUI:
    """Main application window for the password generator."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Random Password Generator")
        self.root.geometry("620x650")
        self.root.minsize(560, 600)

        self.history = PasswordSessionHistory(max_items=5)
        self.current_password = ""

        self.length_var = tk.IntVar(value=16)
        self.uppercase_var = tk.BooleanVar(value=True)
        self.lowercase_var = tk.BooleanVar(value=True)
        self.numbers_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        self.exclude_ambiguous_var = tk.BooleanVar(value=False)

        self.password_var = tk.StringVar(value="")
        self.strength_var = tk.StringVar(value="Strength: —")
        self.status_var = tk.StringVar(value="Ready to generate a password.")

        self._build_interface()

    def _build_interface(self) -> None:
        """Create and arrange all GUI widgets."""
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill="both", expand=True)

        title = ttk.Label(
            main_frame,
            text="Random Password Generator",
            font=("Segoe UI", 20, "bold"),
        )
        title.pack(pady=(0, 5))

        subtitle = ttk.Label(
            main_frame,
            text="Generate secure passwords using Python secrets.",
        )
        subtitle.pack(pady=(0, 20))

        settings_frame = ttk.LabelFrame(
            main_frame,
            text="Password Settings",
            padding=15,
        )
        settings_frame.pack(fill="x", pady=(0, 15))

        ttk.Label(
            settings_frame,
            text="Password Length:",
        ).grid(row=0, column=0, sticky="w", padx=(0, 10), pady=5)

        length_spinbox = ttk.Spinbox(
            settings_frame,
            from_=8,
            to=128,
            textvariable=self.length_var,
            width=8,
        )
        length_spinbox.grid(row=0, column=1, sticky="w", pady=5)

        categories_frame = ttk.LabelFrame(
            settings_frame,
            text="Character Categories",
            padding=10,
        )
        categories_frame.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(10, 5),
        )

        ttk.Checkbutton(
            categories_frame,
            text="Uppercase",
            variable=self.uppercase_var,
        ).grid(row=0, column=0, sticky="w", padx=5, pady=3)

        ttk.Checkbutton(
            categories_frame,
            text="Lowercase",
            variable=self.lowercase_var,
        ).grid(row=0, column=1, sticky="w", padx=5, pady=3)

        ttk.Checkbutton(
            categories_frame,
            text="Numbers",
            variable=self.numbers_var,
        ).grid(row=1, column=0, sticky="w", padx=5, pady=3)

        ttk.Checkbutton(
            categories_frame,
            text="Symbols",
            variable=self.symbols_var,
        ).grid(row=1, column=1, sticky="w", padx=5, pady=3)

        ttk.Checkbutton(
            settings_frame,
            text="Exclude ambiguous characters (0, O, o, 1, I, l)",
            variable=self.exclude_ambiguous_var,
        ).grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="w",
            pady=(10, 5),
        )

        ttk.Button(
            main_frame,
            text="Generate Password",
            command=self.generate,
        ).pack(fill="x", pady=(0, 15))

        result_frame = ttk.LabelFrame(
            main_frame,
            text="Generated Password",
            padding=15,
        )
        result_frame.pack(fill="x", pady=(0, 15))

        password_entry = ttk.Entry(
            result_frame,
            textvariable=self.password_var,
            state="readonly",
            font=("Consolas", 12),
        )
        password_entry.pack(fill="x", pady=(0, 10))

        strength_label = ttk.Label(
            result_frame,
            textvariable=self.strength_var,
            font=("Segoe UI", 11, "bold"),
        )
        strength_label.pack(anchor="w", pady=(0, 10))

        ttk.Button(
            result_frame,
            text="Copy Password",
            command=self.copy_current_password,
        ).pack(fill="x")

        history_frame = ttk.LabelFrame(
            main_frame,
            text="Recent Passwords — Current Session",
            padding=15,
        )
        history_frame.pack(fill="both", expand=True)

        self.history_listbox = tk.Listbox(
            history_frame,
            height=6,
            font=("Consolas", 10),
            activestyle="none",
        )
        self.history_listbox.pack(fill="both", expand=True)

        status_label = ttk.Label(
            main_frame,
            textvariable=self.status_var,
            anchor="w",
        )
        status_label.pack(fill="x", pady=(10, 0))

    def _selected_categories(self) -> dict[str, bool]:
        """Return the selected character categories as boolean flags."""
        return {
            "uppercase": self.uppercase_var.get(),
            "lowercase": self.lowercase_var.get(),
            "numbers": self.numbers_var.get(),
            "symbols": self.symbols_var.get(),
        }

    def generate(self) -> None:
        """Generate a password using the selected GUI settings."""
        try:
            categories = self._selected_categories()

            password = generate_password(
                length=self.length_var.get(),
                categories=categories,
                exclude_ambiguous=self.exclude_ambiguous_var.get(),
            )

            strength, entropy = assess_password_strength(password)

            self.current_password = password
            self.password_var.set(password)
            self.strength_var.set(
                f"Strength: {strength}  |  Estimated entropy: {entropy} bits"
            )

            self.history.add(password)
            self._refresh_history()

            self.status_var.set("Password generated successfully.")

        except (PasswordGenerationError, ValueError, tk.TclError) as error:
            messagebox.showerror("Invalid Settings", str(error))
            self.status_var.set("Please correct the settings and try again.")

    def copy_current_password(self) -> None:
        """Copy the currently generated password to the clipboard."""
        if not self.current_password:
            messagebox.showwarning(
                "No Password",
                "Generate a password before copying it.",
            )
            return

        try:
            copy_password(self.current_password)
            self.status_var.set("Password copied to clipboard.")

        except (ValueError, RuntimeError, OSError) as error:
            messagebox.showerror(
                "Clipboard Error",
                f"Could not copy the password.\n\n{error}",
            )

    def _refresh_history(self) -> None:
        """Refresh the visible session history with masked values."""
        self.history_listbox.delete(0, tk.END)

        for password in self.history.get_recent():
            masked_password = "•" * len(password)
            self.history_listbox.insert(
                tk.END,
                f"{masked_password}  ({len(password)} characters)",
            )


def create_application() -> tuple[tk.Tk, PasswordGeneratorGUI]:
    """Create the Tkinter application and GUI controller."""
    root = tk.Tk()
    application = PasswordGeneratorGUI(root)
    return root, application
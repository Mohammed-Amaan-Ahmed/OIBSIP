"""Tkinter graphical user interface for the BMI Calculator."""

from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk

from .bmi import calculate_bmi_result
from .chart import show_bmi_trend
from .database import get_user_history, initialize_database, save_bmi_record


class BMICalculatorApp:
    """Main BMI Calculator application."""

    CATEGORY_COLORS = {
        "Underweight": "#3498db",
        "Normal": "#27ae60",
        "Overweight": "#f39c12",
        "Obese": "#e74c3c",
    }

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("BMI Calculator")
        self.root.geometry("520x620")
        self.root.resizable(False, False)

        self.name_var = tk.StringVar()
        self.weight_var = tk.StringVar()
        self.height_var = tk.StringVar()

        self.bmi_var = tk.StringVar(value="BMI: —")
        self.category_var = tk.StringVar(value="Category: —")
        self.status_var = tk.StringVar(value="Enter your details to calculate BMI.")

        self._build_interface()

    def _build_interface(self) -> None:
        """Create and arrange all GUI widgets."""
        main_frame = ttk.Frame(self.root, padding=25)
        main_frame.pack(fill="both", expand=True)

        title = ttk.Label(
            main_frame,
            text="BMI Calculator",
            font=("Segoe UI", 22, "bold"),
        )
        title.pack(pady=(0, 5))

        subtitle = ttk.Label(
            main_frame,
            text="Calculate and track your Body Mass Index",
            font=("Segoe UI", 10),
        )
        subtitle.pack(pady=(0, 25))

        form_frame = ttk.LabelFrame(
            main_frame,
            text="Personal Information",
            padding=15,
        )
        form_frame.pack(fill="x")

        ttk.Label(form_frame, text="Name:").grid(
            row=0,
            column=0,
            sticky="w",
            padx=5,
            pady=8,
        )

        self.name_entry = ttk.Entry(
            form_frame,
            textvariable=self.name_var,
            width=35,
        )
        self.name_entry.grid(
            row=0,
            column=1,
            padx=5,
            pady=8,
        )

        ttk.Label(form_frame, text="Weight (kg):").grid(
            row=1,
            column=0,
            sticky="w",
            padx=5,
            pady=8,
        )

        self.weight_entry = ttk.Entry(
            form_frame,
            textvariable=self.weight_var,
            width=35,
        )
        self.weight_entry.grid(
            row=1,
            column=1,
            padx=5,
            pady=8,
        )

        ttk.Label(form_frame, text="Height (m):").grid(
            row=2,
            column=0,
            sticky="w",
            padx=5,
            pady=8,
        )

        self.height_entry = ttk.Entry(
            form_frame,
            textvariable=self.height_var,
            width=35,
        )
        self.height_entry.grid(
            row=2,
            column=1,
            padx=5,
            pady=8,
        )

        calculate_button = ttk.Button(
            main_frame,
            text="Calculate BMI",
            command=self.calculate_and_save,
        )
        calculate_button.pack(pady=20)

        result_frame = ttk.LabelFrame(
            main_frame,
            text="Result",
            padding=20,
        )
        result_frame.pack(fill="x")

        self.bmi_label = tk.Label(
            result_frame,
            textvariable=self.bmi_var,
            font=("Segoe UI", 20, "bold"),
        )
        self.bmi_label.pack(pady=5)

        self.category_label = tk.Label(
            result_frame,
            textvariable=self.category_var,
            font=("Segoe UI", 16, "bold"),
        )
        self.category_label.pack(pady=5)

        status_label = ttk.Label(
            result_frame,
            textvariable=self.status_var,
            wraplength=400,
            justify="center",
        )
        status_label.pack(pady=(10, 5))

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)

        ttk.Button(
            button_frame,
            text="View History",
            command=self.view_history,
        ).grid(row=0, column=0, padx=5)

        ttk.Button(
            button_frame,
            text="View Trend",
            command=self.view_trend,
        ).grid(row=0, column=1, padx=5)

        ttk.Button(
            button_frame,
            text="Clear",
            command=self.clear_fields,
        ).grid(row=0, column=2, padx=5)

        self.name_entry.focus_set()

    def calculate_and_save(self) -> None:
        """Calculate BMI, display the result, and save the record."""
        name = self.name_var.get().strip()
        weight = self.weight_var.get().strip()
        height = self.height_var.get().strip()

        if not name:
            self._show_error("Please enter a name.")
            self.name_entry.focus_set()
            return

        if not weight:
            self._show_error("Please enter your weight in kilograms.")
            self.weight_entry.focus_set()
            return

        if not height:
            self._show_error("Please enter your height in meters.")
            self.height_entry.focus_set()
            return

        try:
            bmi, category = calculate_bmi_result(weight, height)

            recorded_at = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            save_bmi_record(
                name=name,
                weight_kg=float(weight),
                height_m=float(height),
                bmi=bmi,
                category=category,
                recorded_at=recorded_at,
            )

        except ValueError as exc:
            self._show_error(str(exc))
            return

        except RuntimeError as exc:
            self._show_error(
                f"Unable to save your BMI record.\n\n{exc}"
            )
            return

        self.bmi_var.set(f"BMI: {bmi:.2f}")
        self.category_var.set(f"Category: {category}")

        category_color = self.CATEGORY_COLORS.get(
            category,
            "#2c3e50",
        )

        self.category_label.configure(
            foreground=category_color
        )

        self.status_var.set(
            f"Record saved for {name} at {recorded_at}."
        )

    def view_history(self) -> None:
        """Display BMI history for the entered user."""
        name = self.name_var.get().strip()

        if not name:
            self._show_error(
                "Enter a name to view that user's BMI history."
            )
            self.name_entry.focus_set()
            return

        try:
            records = get_user_history(name)

        except ValueError as exc:
            self._show_error(str(exc))
            return

        except RuntimeError as exc:
            self._show_error(
                f"Unable to retrieve BMI history.\n\n{exc}"
            )
            return

        if not records:
            messagebox.showinfo(
                "BMI History",
                f"No BMI records found for {name}.",
            )
            return

        history_window = tk.Toplevel(self.root)
        history_window.title(f"BMI History - {name}")
        history_window.geometry("780x350")
        history_window.resizable(True, True)

        columns = (
            "date",
            "weight",
            "height",
            "bmi",
            "category",
        )

        tree = ttk.Treeview(
            history_window,
            columns=columns,
            show="headings",
        )

        headings = {
            "date": "Recorded At",
            "weight": "Weight (kg)",
            "height": "Height (m)",
            "bmi": "BMI",
            "category": "Category",
        }

        widths = {
            "date": 170,
            "weight": 100,
            "height": 100,
            "bmi": 100,
            "category": 140,
        }

        for column in columns:
            tree.heading(column, text=headings[column])
            tree.column(
                column,
                width=widths[column],
                anchor="center",
            )

        for record in records:
            tree.insert(
                "",
                "end",
                values=(
                    record[6],
                    f"{record[2]:.2f}",
                    f"{record[3]:.2f}",
                    f"{record[4]:.2f}",
                    record[5],
                ),
            )

        scrollbar = ttk.Scrollbar(
            history_window,
            orient="vertical",
            command=tree.yview,
        )

        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(10, 0),
            pady=10,
        )

        scrollbar.pack(
            side="right",
            fill="y",
            pady=10,
            padx=(0, 10),
        )

    def view_trend(self) -> None:
        """Display the BMI trend for the entered user."""
        name = self.name_var.get().strip()

        if not name:
            self._show_error(
                "Enter a name to view that user's BMI trend."
            )
            self.name_entry.focus_set()
            return

        try:
            records = get_user_history(name)
            show_bmi_trend(records)

        except ValueError as exc:
            messagebox.showinfo(
                "BMI Trend",
                str(exc),
            )

        except RuntimeError as exc:
            self._show_error(
                f"Unable to retrieve BMI history.\n\n{exc}"
            )

    def clear_fields(self) -> None:
        """Clear all input and result fields."""
        self.name_var.set("")
        self.weight_var.set("")
        self.height_var.set("")

        self.bmi_var.set("BMI: —")
        self.category_var.set("Category: —")
        self.category_label.configure(
            foreground="#2c3e50"
        )

        self.status_var.set(
            "Enter your details to calculate BMI."
        )

        self.name_entry.focus_set()

    @staticmethod
    def _show_error(message: str) -> None:
        """Display a user-friendly error dialog."""
        messagebox.showerror("BMI Calculator", message)


def create_application() -> tk.Tk:
    """Initialize the database and create the application window."""
    initialize_database()

    root = tk.Tk()
    BMICalculatorApp(root)

    return root
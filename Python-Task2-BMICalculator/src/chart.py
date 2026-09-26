"""BMI trend chart generation using Matplotlib."""

from typing import Sequence, Tuple

import matplotlib.pyplot as plt


def show_bmi_trend(records: Sequence[Tuple]) -> None:
    """
    Display a BMI trend chart for historical records.

    Each record is expected to contain:
        id, name, weight_kg, height_m, bmi, category, recorded_at

    Raises:
        ValueError: If no records are available.
    """
    if not records:
        raise ValueError("No BMI history is available to display.")

    dates = [record[6] for record in records]
    bmi_values = [record[4] for record in records]

    plt.figure(figsize=(9, 5))

    plt.plot(
        dates,
        bmi_values,
        marker="o",
        linewidth=2,
    )

    plt.title("BMI Trend")
    plt.xlabel("Date")
    plt.ylabel("BMI")

    plt.xticks(rotation=45, ha="right")
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()
"""Core BMI calculation and validation logic."""

from typing import Tuple


def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """
    Calculate BMI using weight in kilograms and height in meters.

    Args:
        weight_kg: Person's weight in kilograms.
        height_m: Person's height in meters.

    Returns:
        BMI rounded to two decimal places.

    Raises:
        ValueError: If weight or height is not numeric or is not positive.
    """
    try:
        weight = float(weight_kg)
        height = float(height_m)
    except (TypeError, ValueError) as exc:
        raise ValueError("Weight and height must be numeric values.") from exc

    if weight <= 0:
        raise ValueError("Weight must be greater than zero.")

    if height <= 0:
        raise ValueError("Height must be greater than zero.")

    bmi = weight / (height ** 2)
    return round(bmi, 2)


def get_bmi_category(bmi: float) -> str:
    """
    Determine the BMI category.

    Args:
        bmi: Calculated BMI value.

    Returns:
        BMI category.

    Raises:
        ValueError: If BMI is negative or not numeric.
    """
    try:
        value = float(bmi)
    except (TypeError, ValueError) as exc:
        raise ValueError("BMI must be a numeric value.") from exc

    if value < 0:
        raise ValueError("BMI cannot be negative.")

    if value < 18.5:
        return "Underweight"
    if value < 25:
        return "Normal"
    if value < 30:
        return "Overweight"

    return "Obese"


def calculate_bmi_result(
    weight_kg: float,
    height_m: float,
) -> Tuple[float, str]:
    """
    Calculate BMI and determine its category.

    Returns:
        A tuple containing (BMI, category).
    """
    bmi = calculate_bmi(weight_kg, height_m)
    category = get_bmi_category(bmi)
    return bmi, category
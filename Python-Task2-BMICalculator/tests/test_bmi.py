import unittest

from src.bmi import calculate_bmi, get_bmi_category, calculate_bmi_result


class TestCalculateBMI(unittest.TestCase):

    def test_calculate_bmi(self):
        self.assertEqual(calculate_bmi(70, 1.75), 22.86)

    def test_bmi_rounds_to_two_decimal_places(self):
        self.assertEqual(calculate_bmi(80, 1.80), 24.69)

    def test_zero_weight_rejected(self):
        with self.assertRaises(ValueError):
            calculate_bmi(0, 1.75)

    def test_negative_weight_rejected(self):
        with self.assertRaises(ValueError):
            calculate_bmi(-70, 1.75)

    def test_zero_height_rejected(self):
        with self.assertRaises(ValueError):
            calculate_bmi(70, 0)

    def test_negative_height_rejected(self):
        with self.assertRaises(ValueError):
            calculate_bmi(70, -1.75)

    def test_non_numeric_weight_rejected(self):
        with self.assertRaises(ValueError):
            calculate_bmi("abc", 1.75)

    def test_non_numeric_height_rejected(self):
        with self.assertRaises(ValueError):
            calculate_bmi(70, "abc")


class TestBMICategory(unittest.TestCase):

    def test_underweight(self):
        self.assertEqual(get_bmi_category(18.49), "Underweight")

    def test_normal_lower_boundary(self):
        self.assertEqual(get_bmi_category(18.5), "Normal")

    def test_normal_upper_boundary(self):
        self.assertEqual(get_bmi_category(24.9), "Normal")

    def test_overweight_lower_boundary(self):
        self.assertEqual(get_bmi_category(25.0), "Overweight")

    def test_overweight_upper_boundary(self):
        self.assertEqual(get_bmi_category(29.9), "Overweight")

    def test_obese_boundary(self):
        self.assertEqual(get_bmi_category(30.0), "Obese")

    def test_negative_bmi_rejected(self):
        with self.assertRaises(ValueError):
            get_bmi_category(-1)


class TestBMIResult(unittest.TestCase):

    def test_calculate_bmi_result(self):
        result = calculate_bmi_result(70, 1.75)
        self.assertEqual(result, (22.86, "Normal"))


if __name__ == "__main__":
    unittest.main()
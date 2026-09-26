import unittest
from unittest.mock import patch

from src.chart import show_bmi_trend


class TestBMIChart(unittest.TestCase):

    def test_empty_records_rejected(self):
        with self.assertRaises(ValueError):
            show_bmi_trend([])

    @patch("src.chart.plt.show")
    @patch("src.chart.plt.plot")
    def test_valid_records_generate_chart(
        self,
        mock_plot,
        mock_show,
    ):
        records = [
            (
                1,
                "Amaan",
                70.0,
                1.75,
                22.86,
                "Normal",
                "2026-09-26 22:00:00",
            ),
            (
                2,
                "Amaan",
                72.0,
                1.75,
                23.51,
                "Normal",
                "2026-09-27 22:00:00",
            ),
        ]

        show_bmi_trend(records)

        mock_plot.assert_called_once()
        mock_show.assert_called_once()

        args, kwargs = mock_plot.call_args

        self.assertEqual(
            args[0],
            [
                "2026-09-26 22:00:00",
                "2026-09-27 22:00:00",
            ],
        )

        self.assertEqual(
            args[1],
            [22.86, 23.51],
        )

        self.assertEqual(
            kwargs["marker"],
            "o",
        )

        self.assertEqual(
            kwargs["linewidth"],
            2,
        )


if __name__ == "__main__":
    unittest.main()
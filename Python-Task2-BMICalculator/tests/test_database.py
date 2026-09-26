import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src import database


class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

        self.database_path = (
            Path(self.temp_dir.name) / "test_bmi_records.db"
        )

        self.data_dir = Path(self.temp_dir.name)

        self.patches = (
            patch.object(database, "DATA_DIR", self.data_dir),
            patch.object(database, "DATABASE_PATH", self.database_path),
        )

        for patcher in self.patches:
            patcher.start()

        database.initialize_database()

    def tearDown(self):
        for patcher in reversed(self.patches):
            patcher.stop()

        self.temp_dir.cleanup()

    def test_database_file_created(self):
        self.assertTrue(self.database_path.exists())

    def test_save_bmi_record(self):
        record_id = database.save_bmi_record(
            "Amaan",
            70,
            1.75,
            22.86,
            "Normal",
            "2026-09-26 22:00:00",
        )

        self.assertIsInstance(record_id, int)
        self.assertGreater(record_id, 0)

    def test_get_user_history(self):
        database.save_bmi_record(
            "Amaan",
            70,
            1.75,
            22.86,
            "Normal",
            "2026-09-26 22:00:00",
        )

        history = database.get_user_history("Amaan")

        self.assertEqual(len(history), 1)
        self.assertEqual(history[0][1], "Amaan")
        self.assertEqual(history[0][4], 22.86)
        self.assertEqual(history[0][5], "Normal")

    def test_multiple_records_for_same_user(self):
        database.save_bmi_record(
            "Amaan",
            70,
            1.75,
            22.86,
            "Normal",
            "2026-09-26 22:00:00",
        )

        database.save_bmi_record(
            "Amaan",
            72,
            1.75,
            23.51,
            "Normal",
            "2026-09-27 22:00:00",
        )

        history = database.get_user_history("Amaan")

        self.assertEqual(len(history), 2)
        self.assertEqual(history[0][4], 22.86)
        self.assertEqual(history[1][4], 23.51)

    def test_multiple_users(self):
        database.save_bmi_record(
            "Amaan",
            70,
            1.75,
            22.86,
            "Normal",
            "2026-09-26 22:00:00",
        )

        database.save_bmi_record(
            "Ahmed",
            90,
            1.80,
            27.78,
            "Overweight",
            "2026-09-26 23:00:00",
        )

        amaan_history = database.get_user_history("Amaan")
        ahmed_history = database.get_user_history("Ahmed")

        self.assertEqual(len(amaan_history), 1)
        self.assertEqual(len(ahmed_history), 1)

        self.assertEqual(amaan_history[0][1], "Amaan")
        self.assertEqual(ahmed_history[0][1], "Ahmed")

    def test_empty_name_rejected_when_saving(self):
        with self.assertRaises(ValueError):
            database.save_bmi_record(
                "",
                70,
                1.75,
                22.86,
                "Normal",
                "2026-09-26 22:00:00",
            )

    def test_empty_name_rejected_when_reading(self):
        with self.assertRaises(ValueError):
            database.get_user_history("")

    def test_records_persist_after_reconnecting(self):
        database.save_bmi_record(
            "Amaan",
            70,
            1.75,
            22.86,
            "Normal",
            "2026-09-26 22:00:00",
        )

        connection = database.get_connection()

        try:
            cursor = connection.execute(
                "SELECT COUNT(*) FROM bmi_records"
            )
            count = cursor.fetchone()[0]
        finally:
            connection.close()

        self.assertEqual(count, 1)

    def test_get_all_records(self):
        database.save_bmi_record(
            "Amaan",
            70,
            1.75,
            22.86,
            "Normal",
            "2026-09-26 22:00:00",
        )

        database.save_bmi_record(
            "Ahmed",
            90,
            1.80,
            27.78,
            "Overweight",
            "2026-09-26 23:00:00",
        )

        records = database.get_all_records()

        self.assertEqual(len(records), 2)
        self.assertEqual(records[0][1], "Amaan")
        self.assertEqual(records[1][1], "Ahmed")


if __name__ == "__main__":
    unittest.main()
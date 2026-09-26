"""SQLite database operations for BMI records."""

import sqlite3
from pathlib import Path
from typing import List, Tuple


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATABASE_PATH = DATA_DIR / "bmi_records.db"


def get_connection() -> sqlite3.Connection:
    """Create and return a connection to the BMI database."""
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(DATABASE_PATH)
        connection.row_factory = sqlite3.Row
        return connection
    except sqlite3.Error as exc:
        raise RuntimeError("Unable to connect to the BMI database.") from exc


def initialize_database() -> None:
    """Create the BMI records table if it does not already exist."""
    connection = get_connection()

    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS bmi_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                weight_kg REAL NOT NULL,
                height_m REAL NOT NULL,
                bmi REAL NOT NULL,
                category TEXT NOT NULL,
                recorded_at TEXT NOT NULL
            )
            """
        )
        connection.commit()
    except sqlite3.Error as exc:
        connection.rollback()
        raise RuntimeError("Unable to initialize the BMI database.") from exc
    finally:
        connection.close()


def save_bmi_record(
    name: str,
    weight_kg: float,
    height_m: float,
    bmi: float,
    category: str,
    recorded_at: str,
) -> int:
    """Save a BMI record and return its generated database ID."""
    if not name.strip():
        raise ValueError("Name cannot be empty.")

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO bmi_records
            (name, weight_kg, height_m, bmi, category, recorded_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                name.strip(),
                weight_kg,
                height_m,
                bmi,
                category,
                recorded_at,
            ),
        )

        connection.commit()
        return int(cursor.lastrowid)

    except sqlite3.Error as exc:
        connection.rollback()
        raise RuntimeError("Unable to save the BMI record.") from exc

    finally:
        connection.close()


def get_user_history(name: str) -> List[Tuple]:
    """Return BMI records belonging to a specific user."""
    if not name.strip():
        raise ValueError("Name cannot be empty.")

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            SELECT id, name, weight_kg, height_m, bmi, category, recorded_at
            FROM bmi_records
            WHERE name = ?
            ORDER BY recorded_at ASC, id ASC
            """,
            (name.strip(),),
        )

        return [tuple(row) for row in cursor.fetchall()]

    except sqlite3.Error as exc:
        raise RuntimeError("Unable to retrieve BMI history.") from exc

    finally:
        connection.close()


def get_all_records() -> List[Tuple]:
    """Return all BMI records ordered chronologically."""
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            SELECT id, name, weight_kg, height_m, bmi, category, recorded_at
            FROM bmi_records
            ORDER BY recorded_at ASC, id ASC
            """
        )

        return [tuple(row) for row in cursor.fetchall()]

    except sqlite3.Error as exc:
        raise RuntimeError("Unable to retrieve BMI records.") from exc

    finally:
        connection.close()
import tempfile
import unittest
from src.db.backend.file_database import FileDatabase
from src.db.backend.errors import TableNotFoundError

class TestFileDatabase(unittest.TestCase):
    def test_data_is_saved_between_instances(self):
        with tempfile.TemporaryDirectory() as directory:
            first_db = FileDatabase(directory)
            first_db.create_table("students")
            first_db.create_record("students", 1, "Иван", "Петров", 20, "M")

            second_db = FileDatabase(directory)
            results = second_db.select_records("students")

            self.assertEqual(len(results), 1)
            self.assertEqual(results[0][1], "Иван")

    def test_select_with_filters(self):
        with tempfile.TemporaryDirectory() as directory:
            db = FileDatabase(directory)
            db.create_table("students")
            db.create_record("students", 1, "Иван", "Петров", 20, "M")
            db.create_record("students", 2, "Мария", "Иванова", 22, "F")

            results = db.select_records("students", first_name="Мария")

            self.assertEqual(len(results), 1)
            self.assertEqual(results[0][2], "Иванова")

    def test_select_from_missing_table(self):
        with tempfile.TemporaryDirectory() as directory:
            db = FileDatabase(directory)

            with self.assertRaises(TableNotFoundError):
                db.select_records("students")
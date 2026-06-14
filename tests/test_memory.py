import unittest
from src.db.backend.memory import StudentTable, MemoryDatabase
from src.db.backend.errors import (
    InvalidAgeError,
    DuplicateIDError,
    TableAlreadyExistsError,
    TableNotFoundError
)

class TestMemory(unittest.TestCase):
    def setUp(self):
        self.table = StudentTable()

    def test_create_record(self):
        record = self.table.create_record(1, "Иван", "Петров", 20, "M")
        self.assertEqual(record, (1, "Иван", "Петров", 20, "M"))

    def test_create_record_negative_age(self):
        with self.assertRaises(InvalidAgeError):
            self.table.create_record(1, "Иван", "Петров", -5, "M")

    def test_create_record_duplicate_id(self):
        self.table.create_record(1, "Иван", "Петров", 20, "M")
        with self.assertRaises(DuplicateIDError):
            self.table.create_record(1, "Мария", "Иванова", 22, "F")

    def test_select_record_no_filters(self):
        self.table.create_record(1, "Иван", "Петров", 20, "M")
        self.table.create_record(2, "Мария", "Иванова", 22, "F")
        results = self.table.select_record()
        self.assertEqual(len(results), 2)

    def test_select_record_by_id(self):
        self.table.create_record(1, "Иван", "Петров", 20, "M")
        self.table.create_record(2, "Мария", "Иванова", 22, "F")
        results = self.table.select_record(student_id=1)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][1], "Иван")

    def test_select_by_second_name(self):
        self.table.create_record(1, "Иван", "Петров", 20, "M")
        self.table.create_record(2, "Мария", "Иванова", 22, "F")
        results = self.table.select_record(second_name="Петров")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][1], "Иван")

    def test_select_by_age(self):
        self.table.create_record(1, "Иван", "Петров", 20, "M")
        self.table.create_record(2, "Мария", "Иванова", 22, "F")
        results = self.table.select_record(age=20)
        self.assertEqual(len(results), 1)

    def test_select_by_sex(self):
        self.table.create_record(1, "Иван", "Петров", 20, "M")
        self.table.create_record(2, "Мария", "Иванова", 22, "F")
        results = self.table.select_record(sex="F")
        self.assertEqual(len(results), 1)

    def test_select_empty_result(self):
        results = self.table.select_record(first_name="Nonexistent")
        self.assertEqual(results, [])

    def test_update_record(self):
        self.table.create_record(1, "Иван", "Петров", 20, "M")
        updated = self.table.update_record(1, first_name="Пётр")
        self.assertEqual(updated[1], "Пётр")

    def test_delete_record(self):
        self.table.create_record(1, "Иван", "Петров", 20, "M")
        self.table.delete_record(1)
        results = self.table.select_record()
        self.assertEqual(len(results), 0)


class TestMemoryDatabase(unittest.TestCase):
    def setUp(self):
        self.db = MemoryDatabase()

    def test_create_table(self):
        self.db.create_table("students")
        self.assertIn("students", self.db.tables)

    def test_create_table_already_exists(self):
        self.db.create_table("students")
        with self.assertRaises(TableAlreadyExistsError):
            self.db.create_table("students")

    def test_create_record(self):
        self.db.create_table("students")
        record = self.db.create_record("students", 1, "Иван", "Петров", 20, "M")
        self.assertEqual(record[1], "Иван")

    def test_select_records(self):
        self.db.create_table("students")
        self.db.create_record("students", 1, "Иван", "Петров", 20, "M")
        results = self.db.select_records("students", first_name="Иван")
        self.assertEqual(len(results), 1)

    def test_update_record(self):
        self.db.create_table("students")
        self.db.create_record("students", 1, "Иван", "Петров", 20, "M")
        updated = self.db.update_record("students", 1, first_name="Пётр")
        self.assertEqual(updated[1], "Пётр")

    def test_delete_record(self):
        self.db.create_table("students")
        self.db.create_record("students", 1, "Иван", "Петров", 20, "M")
        self.db.delete_record("students", 1)
        results = self.db.select_records("students")
        self.assertEqual(len(results), 0)

    def test_table_not_found(self):
        with self.assertRaises(TableNotFoundError):
            self.db.select_records("nonexistent")
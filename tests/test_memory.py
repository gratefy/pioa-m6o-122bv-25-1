import unittest
from src.db.backend.memory import StudentTable
from src.db.backend.errors import InvalidAgeError, DuplicateIDError

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
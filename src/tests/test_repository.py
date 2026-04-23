import pytest
from src.db.models import Student
from src.db.repository import StudentRepository

class TestStudentRepository:
    def setup_method(self):
        self.repo = StudentRepository()

    def test_add_student(self):
        s = Student(first_name="Иван", second_name="Петров", age=20, sex="M")
        saved = self.repo.add(s)
        assert saved.id == 1
        assert self.repo.get_by_id(1) == saved

    def test_add_raises_if_no_name(self):
        with pytest.raises(ValueError):
            self.repo.add(Student(first_name="", second_name="Тестов"))

    def test_get_all_empty(self):
        assert self.repo.get_all() == []

    def test_update_student(self):
        s = Student(first_name="Анна", second_name="Иванова", age=19, sex="F")
        self.repo.add(s)
        updated = self.repo.update(1, age=20)
        assert updated.age == 20

    def test_delete_student(self):
        s = Student(first_name="Пётр", second_name="Сидоров", age=22, sex="M")
        self.repo.add(s)
        self.repo.delete(1)
        assert self.repo.get_by_id(1) is None

    def test_filter(self):
        self.repo.add(Student(first_name="А", second_name="Б", age=18, sex="M"))
        self.repo.add(Student(first_name="В", second_name="Г", age=20, sex="F"))
        filtered = self.repo.filter(age=18)
        assert len(filtered) == 1
        assert filtered[0].age == 18

    def test_sorted(self):
        self.repo.add(Student(first_name="Иван", second_name="А", age=30, sex="M"))
        self.repo.add(Student(first_name="Анна", second_name="Б", age=20, sex="F"))
        self.repo.add(Student(first_name="Пётр", second_name="В", age=25, sex="M"))
        
        sorted_by_age = self.repo.get_sorted("age")
        ages = [s.age for s in sorted_by_age]
        assert ages == [20, 25, 30]
        
        sorted_by_age_desc = self.repo.get_sorted("age", reverse=True)
        ages_desc = [s.age for s in sorted_by_age_desc]
        assert ages_desc == [30, 25, 20]
        
        sorted_by_name = self.repo.get_sorted("first_name")
        names = [s.first_name for s in sorted_by_name]
        assert names == ["Анна", "Иван", "Пётр"]
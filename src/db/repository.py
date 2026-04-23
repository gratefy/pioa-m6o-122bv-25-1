from typing import List, Optional
from .models import Student

class StudentRepository:
    def __init__(self):
        self._storage: dict[int, Student] = {}
        self._next_id = 1

    def add(self, student: Student) -> Student:
        if not student.first_name or not student.second_name:
            raise ValueError("Имя и фамилия обязательны")
        student.id = self._next_id
        self._storage[self._next_id] = student
        self._next_id += 1
        return student

    def get_all(self) -> List[Student]:
        return list(self._storage.values())

    def get_by_id(self, student_id: int) -> Optional[Student]:
        return self._storage.get(student_id)

    def filter(self, **filters) -> List[Student]:
        result = self.get_all()
        for field, value in filters.items():
            if value is not None:
                result = [s for s in result if getattr(s, field) == value]
        return result

    def update(self, student_id: int, **updates) -> Student:
        student = self.get_by_id(student_id)
        if not student:
            raise KeyError(f"Студент с id {student_id} не найден")
        for key, value in updates.items():
            if hasattr(student, key) and value is not None:
                setattr(student, key, value)
        return student

    def delete(self, student_id: int) -> bool:
        if student_id not in self._storage:
            raise KeyError(f"Студент с id {student_id} не найден")
        del self._storage[student_id]
        return True

    def get_sorted(self, key: str, reverse: bool = False) -> List[Student]:
        """Возвращает отсортированный список студентов по указанному полю"""
        students = self.get_all()
        return sorted(students, key=lambda s: getattr(s, key), reverse=reverse)
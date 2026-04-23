from .repository import StudentRepository
from .models import Student

class StudentCLI:
    def __init__(self):
        self.repo = StudentRepository()

    def _print_menu(self):
        print("\n=== База студентов ===")
        print("1. Добавить студента")
        print("2. Показать всех")
        print("3. Найти по ID")
        print("4. Фильтровать")
        print("5. Обновить студента")
        print("6. Удалить студента")
        print("7. Сортировка по полю")
        print("0. Выход")

    def _read_int(self, prompt: str) -> int:
        while True:
            raw = input(prompt).strip()
            try:
                return int(raw)
            except ValueError:
                print("Ошибка: введите число")

    def _read_optional_int(self, prompt: str) -> int | None:
        while True:
            raw = input(prompt).strip()
            if raw == "":
                return None
            try:
                return int(raw)
            except ValueError:
                print("Ошибка: введите число или Enter")

    def _add_student(self):
        print("\nДобавление студента")
        first_name = input("Имя: ").strip()
        second_name = input("Фамилия: ").strip()
        age = self._read_int("Возраст: ")
        sex = input("Пол (M/F): ").strip()
        try:
            student = Student(first_name=first_name, second_name=second_name, age=age, sex=sex)
            saved = self.repo.add(student)
            print(f"Добавлен студент с ID: {saved.id}")
        except ValueError as e:
            print(f"Ошибка: {e}")

    def _show_all(self):
        students = self.repo.get_all()
        if not students:
            print("Нет студентов")
            return
        for s in students:
            print(f"{s.id}: {s.first_name} {s.second_name}, {s.age} лет, {s.sex}")

    def _find_by_id(self):
        sid = self._read_int("ID студента: ")
        student = self.repo.get_by_id(sid)
        if student:
            print(f"{student.id}: {student.first_name} {student.second_name}, {student.age} лет, {student.sex}")
        else:
            print(f"Студент с ID {sid} не найден")

    def _filter_students(self):
        print("\nФильтрация (Enter = не фильтровать)")
        first_name = input("Имя: ").strip() or None
        second_name = input("Фамилия: ").strip() or None
        age = self._read_optional_int("Возраст: ")
        sex = input("Пол (M/F): ").strip() or None
        results = self.repo.filter(first_name=first_name, second_name=second_name, age=age, sex=sex)
        if results:
            for s in results:
                print(f"{s.id}: {s.first_name} {s.second_name}, {s.age} лет, {s.sex}")
        else:
            print("Не найдено")

    def _update_student(self):
        sid = self._read_int("ID студента для обновления: ")
        student = self.repo.get_by_id(sid)
        if not student:
            print(f"Студент с ID {sid} не найден")
            return
        print(f"Текущие данные: {student.first_name} {student.second_name}, {student.age} лет")
        first_name = input("Новое имя (Enter = оставить): ").strip() or None
        second_name = input("Новая фамилия (Enter = оставить): ").strip() or None
        age = self._read_optional_int("Новый возраст (Enter = оставить): ")
        sex = input("Новый пол (Enter = оставить): ").strip() or None
        try:
            self.repo.update(sid, first_name=first_name, second_name=second_name, age=age, sex=sex)
            print("Обновлено")
        except KeyError as e:
            print(f"{e}")

    def _delete_student(self):
        sid = self._read_int("ID студента для удаления: ")
        confirm = input(f"Удалить студента с ID {sid}? (y/N): ").strip().lower()
        if confirm != 'y':
            print("Отменено")
            return
        try:
            self.repo.delete(sid)
            print("Удалено")
        except KeyError as e:
            print(f"{e}")

    def _sort_students(self):
        print("\nСортировка")
        print("Доступные поля: first_name, second_name, age, sex")
        key = input("Поле для сортировки: ").strip()
        if key not in ["first_name", "second_name", "age", "sex"]:
            print(f"Поле '{key}' не существует")
            return
        reverse = input("По убыванию? (y/N): ").strip().lower() == 'y'
        try:
            sorted_list = self.repo.get_sorted(key, reverse)
            if not sorted_list:
                print("Нет студентов")
                return
            for s in sorted_list:
                print(f"{s.id}: {s.first_name} {s.second_name}, {s.age} лет, {s.sex}")
        except AttributeError:
            print(f"Поле '{key}' не существует")

    def run(self):
        while True:
            self._print_menu()
            choice = input("Выберите действие: ").strip()
            if choice == "1":
                self._add_student()
            elif choice == "2":
                self._show_all()
            elif choice == "3":
                self._find_by_id()
            elif choice == "4":
                self._filter_students()
            elif choice == "5":
                self._update_student()
            elif choice == "6":
                self._delete_student()
            elif choice == "7":
                self._sort_students()
            elif choice == "0":
                print("До свидания!")
                break
            else:
                print("Неизвестная команда")


def run():
    cli = StudentCLI()
    cli.run()
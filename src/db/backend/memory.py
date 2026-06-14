from .errors import DuplicateIDError, InvalidAgeError

type StudentRecord = tuple[int, str, str, int, str]

class StudentTable:
    def __init__(self) -> None:
        self._student: list[StudentRecord] = []

    def create_record(
        self,
        student_id: int,
        first_name: str,
        second_name: str,
        age: int,
        sex: str,
    ) -> StudentRecord:
        if age < 0:
            raise InvalidAgeError("Поле age не может быть отрицательным.")

        if any(record[0] == student_id for record in self._student):
            raise DuplicateIDError(f"Запись с id={student_id} уже существует.")

        new_record: StudentRecord = (
            student_id,
            first_name.strip(),
            second_name.strip(),
            age,
            sex.strip(),
        )
        self._student.append(new_record)
        return new_record

    def select_record(
        self,
        student_id: int | None = None,
        first_name: str | None = None,
        second_name: str | None = None,
        age: int | None = None,
        sex: str | None = None,
    ) -> list[StudentRecord]:
        if (
            student_id is None
            and first_name is None
            and second_name is None
            and age is None
            and sex is None
        ):
            return self._student.copy()

        result: list[StudentRecord] = []

        for record in self._student:
            if student_id is not None and record[0] != student_id:
                continue
            if first_name is not None and record[1] != first_name:
                continue
            if second_name is not None and record[2] != second_name:
                continue
            if age is not None and record[3] != age:
                continue
            if sex is not None and record[4] != sex:
                continue
            result.append(record)

        return result

    def update_record(
        self,
        student_id: int,
        first_name: str | None = None,
        second_name: str | None = None,
        age: int | None = None,
        sex: str | None = None,
    ) -> StudentRecord:
        for i, record in enumerate(self._student):
            if record[0] == student_id:
                updated_record = list(record)

                if first_name is not None:
                    updated_record[1] = first_name.strip()
                if second_name is not None:
                    updated_record[2] = second_name.strip()
                if age is not None:
                    if age < 0:
                        raise InvalidAgeError("Поле age не может быть отрицательным.")
                    updated_record[3] = age
                if sex is not None:
                    updated_record[4] = sex.strip()
                self._student[i] = tuple(updated_record)
                return self._student[i]

        raise KeyError(f"Запись с id={student_id} не найдена.")

    def delete_record(self, student_id: int) -> None:
        for i, record in enumerate(self._student):
            if record[0] == student_id:
                del self._student[i]
                return
        raise KeyError(f"Запись с id={student_id} не найдена.")


class MemoryDatabase:
    """In-memory БД с поддержкой нескольких таблиц."""

    def __init__(self):
        self.tables: dict[str, StudentTable] = {}

    def create_table(self, table_name: str) -> None:
        if table_name in self.tables:
            raise Exception(f"Таблица '{table_name}' уже существует")
        self.tables[table_name] = StudentTable()

    def create_record(self, table_name: str, *args) -> StudentRecord:
        if table_name not in self.tables:
            raise Exception(f"Таблица '{table_name}' не существует")
        return self.tables[table_name].create_record(*args)

    def select_records(self, table_name: str, **filters) -> list[StudentRecord]:
        if table_name not in self.tables:
            raise Exception(f"Таблица '{table_name}' не существует")
        return self.tables[table_name].select_record(**filters)

    def update_record(self, table_name: str, student_id: int, **updates) -> StudentRecord:
        if table_name not in self.tables:
            raise Exception(f"Таблица '{table_name}' не существует")
        return self.tables[table_name].update_record(student_id, **updates)

    def delete_record(self, table_name: str, student_id: int) -> None:
        if table_name not in self.tables:
            raise Exception(f"Таблица '{table_name}' не существует")
        return self.tables[table_name].delete_record(student_id)
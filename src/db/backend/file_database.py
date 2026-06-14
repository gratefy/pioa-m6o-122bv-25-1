import json
from pathlib import Path
from .memory import StudentTable
from .errors import (
    TableNotFoundError,
    InvalidStorageDataError,
    TableAlreadyExistsError
)

type StudentRecord = tuple[int, str, str, int, str]

class FileDatabase:
    def __init__(self, directory: str = "data") -> None:
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self.tables: dict[str, StudentTable] = {}

    def _get_table_path(self, table_name: str) -> Path:
        return self.directory / f"{table_name}.json"

    def _validate_record(self, record: list) -> bool:
        return (isinstance(record, list) and len(record) == 5 and
                isinstance(record[0], int) and isinstance(record[1], str) and
                isinstance(record[2], str) and isinstance(record[3], int) and
                isinstance(record[4], str))

    def _load_table_from_disk(self, table_name: str) -> StudentTable:
        path = self._get_table_path(table_name)
        if not path.exists():
            raise TableNotFoundError(f"Таблица '{table_name}' не существует.")
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            raise InvalidStorageDataError(f"Ошибка чтения файла {path}: {e}")
        if "schema" not in data or "records" not in data:
            raise InvalidStorageDataError("Некорректная структура файла")
        if not isinstance(data["records"], list):
            raise InvalidStorageDataError("records должен быть списком")
        table = StudentTable()
        for record in data["records"]:
            if not self._validate_record(record):
                raise InvalidStorageDataError(f"Некорректная запись: {record}")
            table.create_record(*record)
        return table

    def _save_table_to_disk(self, table_name: str, table: StudentTable) -> None:
        path = self._get_table_path(table_name)
        data = {"schema": ["student_id", "first_name", "second_name", "age", "sex"],
                "records": table.get_records()}
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError as e:
            raise InvalidStorageDataError(f"Ошибка записи файла {path}: {e}")

    def create_table(self, table_name: str) -> None:
        if table_name in self.tables:
            raise TableAlreadyExistsError(f"Таблица '{table_name}' уже существует")
        if self._get_table_path(table_name).exists():
            self.tables[table_name] = self._load_table_from_disk(table_name)
        else:
            self.tables[table_name] = StudentTable()
            self._save_table_to_disk(table_name, self.tables[table_name])

    def _get_table(self, table_name: str) -> StudentTable:
        if table_name not in self.tables:
            self.tables[table_name] = self._load_table_from_disk(table_name)
        return self.tables[table_name]

    def create_record(self, table_name: str, *args) -> StudentRecord:
        table = self._get_table(table_name)
        record = table.create_record(*args)
        self._save_table_to_disk(table_name, table)
        return record

    def select_records(self, table_name: str, **filters) -> list[StudentRecord]:
        table = self._get_table(table_name)
        return table.select_record(**filters)

    def update_record(self, table_name: str, student_id: int, **updates) -> StudentRecord:
        table = self._get_table(table_name)
        updated = table.update_record(student_id, **updates)
        self._save_table_to_disk(table_name, table)
        return updated

    def delete_record(self, table_name: str, student_id: int) -> None:
        table = self._get_table(table_name)
        table.delete_record(student_id)
        self._save_table_to_disk(table_name, table)

import json
from pathlib import Path
from .memory import StudentTable
from .errors import TableNotFoundError, InvalidStorageDataError

type StudentRecord = tuple[int, str, str, int, str]

class FileDatabase:
    """Файловая СУБД, сохраняющая таблицы в JSON."""

    def __init__(self, directory: str = "data") -> None:
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self._tables: dict[str, StudentTable] = {}

    def _get_table_path(self, table_name: str) -> Path:
        return self.directory / f"{table_name}.json"

    def _load_table_from_disk(self, table_name: str) -> StudentTable:
        path = self._get_table_path(table_name)
        if not path.exists():
            raise TableNotFoundError(f"Таблица '{table_name}' не существует.")

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            raise InvalidStorageDataError(f"Ошибка чтения файла {path}: {e}")

        table = StudentTable()
        for record in data.get("records", []):
            table.create_record(*record)
        return table

    def _save_table_to_disk(self, table_name: str, table: StudentTable) -> None:
        path = self._get_table_path(table_name)
        data = {
            "records": table._student
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def create_table(self, table_name: str) -> None:
        """Создаёт новую таблицу."""
        if table_name in self._tables:
            print(f"Таблица '{table_name}' уже существует")
            return
        self._tables[table_name] = StudentTable()
        self._save_table_to_disk(table_name, self._tables[table_name])

    def get_table(self, table_name: str) -> StudentTable:
        """Возвращает таблицу (из памяти или с диска)."""
        if table_name not in self._tables:
            self._tables[table_name] = self._load_table_from_disk(table_name)
        return self._tables[table_name]

    def create_record(self, table_name: str, *args) -> StudentRecord:
        table = self.get_table(table_name)
        record = table.create_record(*args)
        self._save_table_to_disk(table_name, table)
        return record

    def select_records(self, table_name: str, **filters) -> list[StudentRecord]:
        table = self.get_table(table_name)
        return table.select_record(**filters)
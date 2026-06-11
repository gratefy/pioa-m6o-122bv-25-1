from abc import ABC, abstractmethod
from typing import Any

class Database(ABC):

    @abstractmethod
    def create_table(self, table_name: str) -> None:
        pass

    @abstractmethod
    def create_record(self, table_name: str, *args) -> Any:
        pass

    @abstractmethod
    def select_records(self, table_name: str, **filters) -> list:
        pass
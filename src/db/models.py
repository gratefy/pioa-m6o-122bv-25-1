from dataclasses import dataclass
from typing import Optional

@dataclass
class Student:
    id: Optional[int] = None
    first_name: str = ""
    second_name: str = ""
    age: int = 0
    sex: str = ""

    def __post_init__(self):
        if self.age < 0:
            raise ValueError("Возраст не может быть отрицательным")
        if self.sex not in ("M", "F", "m", "f"):
            raise ValueError("Пол должен быть M или F")
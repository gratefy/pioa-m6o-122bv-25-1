Головко Евгений Максимович
М6О-122БВ-25
Python

task3
Выполненные задачи

- Переписана с использованием классов
- Сохранена вся функциональность CRUD
- Тесты
- Классовый интерфейс StudentCLI
- Сортировка записей по любому полю (возрастание/убывание)

Структура проекта -
src/
├── db/
│ ├── models.py # dataclass Student
│ ├── repository.py # StudentRepository (CRUD + сортировка)
│ ├── cli.py # StudentCLI (консольный интерфейс)
│ └── main.py # точка входа
└── tests/
└── test_repository.py # 8 тестов

Запуск - python -m src.db
Запуск тестов - pytest

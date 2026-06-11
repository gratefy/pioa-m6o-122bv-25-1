Головко Евгений Максимович
М6О-122БВ-25
Python

Реализована система управления данными с поддержкой двух типов баз данных:

1: In-memory — данные хранятся в оперативной памяти (теряются после выхода)
2: File database (JSON) — данные сохраняются в файлы на диске и не теряются
Структура:
pioa-m6o-122bv-25-1/
src/
├── db/
│ ├── main.py # точка входа
│ ├── tui.py # интерфейс
│ └── backend/
│ ├── memory.py # in-memory БД
│ ├── file_database.py # файловая БД (JSON)
│ ├── database.py # общий интерфейс
│ └── errors.py # исключения
tests/
├── test_memory.py
└── test_file_database.py

Запуск - python -m src.db
Запуск тестов - python -m unittest discover -s tests

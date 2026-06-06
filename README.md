Головко Евгений Максимович
М6О-122БВ-25
Python

Реализована система управления данными с поддержкой двух типов баз данных:

1: In-memory — данные хранятся в оперативной памяти (теряются после выхода)
2: File database (JSON) — данные сохраняются в файлы на диске и не теряются
Структура:
pioa-m6o-122bv-25-1/
│
├── src/
│ └── db/
│ ├── backend/
│ │ ├── init.py
│ │ ├── memory.py # In-memory реализация (StudentTable)
│ │ ├── file_database.py # Файловая реализация (JSON)
│ │ └── errors.py # Пользовательские исключения
│ ├── init.py
│ ├── main.py # Точка входа
│ └── tui.py # Текстовый интерфейс пользователя
│
├── data/ # Папка с JSON-файлами таблиц
│
├── tests/
│ └── test_memory.py # Тесты для in-memory БД
│
└── README.md

Запуск - python -m src.db
Запуск тестов - python -m unittest discover -s tests

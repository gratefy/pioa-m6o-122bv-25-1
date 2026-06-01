Головко Евгений Максимович
М6О-122БВ-25
Python

Прототип базы данных, работающей в оперативной памяти.  
Реализована на Python с использованием ООП и TDD.
Структура проекта:
pioa-m6o-122bv-25-1/
│
├── src/
│ └── db/
│ └── backend/
│ ├── init.py
│ ├── errors.py # пользовательские исключения
│ └── memory.py # класс StudentTable
│
├── tests/
│ ├── init.py
│ └── test_memory.py # unittest тесты
│
├── README.md
└── .gitignore

Запуск проекте:
python -m src.db
Запуск теста:
python -m unittest discover -s tests

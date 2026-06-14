Головко Евгений Максимович
М6О-122БВ-25
Python

## Структура проекта

```
src/
└── db/
    ├── __main__.py              # точка входа
    ├── tui.py                   # консольный интерфейс
    └── backend/
        ├── memory.py            # MemoryDatabase + StudentTable
        ├── file_database.py     # FileDatabase
        └── errors.py            # исключения
tests/
├── test_memory.py
└── test_file_database.py
```

---

## Функциональность

- Создание таблиц
- Добавление записей
- Поиск с фильтрацией по любому полю
- Обновление записей
- Удаление записей
- Сохранение на диск (JSON)
- Загрузка данных при запуске

---

## Запуск

```bash
python -m src.db
```

---

## Тесты

```bash
python -m unittest discover -s tests
```

---

## Формат хранения (JSON)

```json
{
  "schema": ["student_id", "first_name", "second_name", "age", "sex"],
  "records": [[1, "Иван", "Петров", 20, "M"]]
}
```
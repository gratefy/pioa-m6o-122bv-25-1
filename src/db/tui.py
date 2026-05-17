from .backend.memory import create_record, select_record, update_record, delete_record
# Функция вывода текстового меню в консоль.
def _print_menu() -> None:
    print("\n=== База студентов ===")
    print("1. Добавить запись")
    print("2. Показать все записи")
    print("3. Найти записи по фильтру")
    print("4. Обновить запись")    # Добавить
    print("5. Удалить запись")      # Добавить
    print("0. Выход")

# Функция чтения целочисленного значения из консоли.
def _read_int(prompt: str) -> int:
    # Используется цикл с повторением до получения корректного ввода.
    while True:
        # Получение строки из консоли с удалением пробельных символов
        # в начале и в конце строки.
        raw = input(prompt).strip()
        try:
            # Преобразование строки к целому числу.
            return int(raw)
        except ValueError:
            # Исключение возникает при невозможности преобразования.
            # Пользователю выводится сообщение об ошибке,
            # после чего ввод повторяется.
            print("Ошибка: введите целое число.")

# Функция добавления новой записи в базу данных.
def _add_student() -> None:
    print("\nДобавление записи")

    student_id = _read_int("id: ")
    first_name = input("first_name: ").strip()
    second_name = input("second_name: ").strip()
    age = _read_int("age: ")
    sex = input("sex: ").strip()

    try:
        # Вызов функции слоя бизнес-логики.
        record = create_record(student_id, first_name, second_name, age, sex)

        # В случае успешного добавления запись выводится в консоль.
        print(f"Запись добавлена: {record}")

    except ValueError as exc:
        # Обработка ошибок валидации.
        print(f"Ошибка: {exc}")

# Вспомогательная функция вывода списка записей.
def _print_records(records: list[tuple[int, str, str, int, str]]) -> None:
    # Проверка на пустой список.
    if not records:
        print("Записи не найдены.")
        return

    # Последовательный вывод записей.
    for record in records:
        print(record)

# Функция вывода всех записей из базы данных.
def _show_all_students() -> None:
    print("\nСписок записей")
    _print_records(select_record())

# Функция чтения необязательного целочисленного значения.
# Пустой ввод интерпретируется как отсутствие фильтра (None).
def _read_optional_int(prompt: str) -> int | None:
    while True:
        raw = input(prompt).strip()

        if raw == "":
            return None

        try:
            return int(raw)
        except ValueError:
            print("Ошибка: введите целое число или оставьте поле пустым.")

def _find_students_by_filter() -> None:
    print("\nПоиск по фильтру (Enter = пропустить поле)")

    student_id = _read_optional_int("id: ")

    first_name = input("first_name: ").strip() or None
    second_name = input("second_name: ").strip() or None

    age = _read_optional_int("age: ")
    sex = input("sex: ").strip() or None

    records = select_record(
        student_id=student_id,
        first_name=first_name,
        second_name=second_name,
        age=age,
        sex=sex,
    )

    _print_records(records)

def run() -> None:
    while True:
        _print_menu()
        action = input("Выберите действие: ").strip()
        
        if action == "1":
            _add_student()
        elif action == "2":
            _show_all_students()
        elif action == "3":
            _find_students_by_filter()
        elif action == "4":          
            _update_student()
        elif action == "5":           
            _delete_student()
        elif action == "0":
            print("Выход из программы.")
            break
        else:
            print("Неизвестная команда. Повторите ввод.")

def _update_student() -> None:
    """Обновление существующей записи"""
    print("\nОбновление записи")
    
    student_id = _read_int("Введите ID записи для обновления: ")
    
    # Показываем текущую запись
    records = select_record(student_id=student_id)
    if not records:
        print(f"Запись с ID {student_id} не найдена.")
        return
    
    print(f"Текущая запись: {records[0]}")
    print("(Оставьте поле пустым, чтобы не менять)")
    
    first_name = input("Новое имя (Enter - пропустить): ").strip() or None
    second_name = input("Новая фамилия (Enter - пропустить): ").strip() or None
    
    age = _read_optional_int("Новый возраст (Enter - пропустить): ")
    sex = input("Новый пол (Enter - пропустить): ").strip() or None
    
    try:
        updated = update_record(student_id, first_name, second_name, age, sex)
        print(f"Запись обновлена: {updated}")
    except KeyError as exc:
        print(f"Ошибка: {exc}")
    except ValueError as exc:
        print(f"Ошибка: {exc}")

def _delete_student() -> None:
    """Удаление записи"""
    print("\nУдаление записи")
    
    student_id = _read_int("Введите ID записи для удаления: ")
    
    # Подтверждение удаления
    confirm = input(f"Вы уверены, что хотите удалить запись с ID {student_id}? (y/N): ").strip().lower()
    
    if confirm != 'y':
        print("Удаление отменено.")
        return
    
    try:
        delete_record(student_id)
        print(f"Запись с ID {student_id} успешно удалена.")
    except KeyError as exc:
        print(f"Ошибка: {exc}")
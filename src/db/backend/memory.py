type StudentRecord = tuple[int, str, str, int, str]
Student: list[StudentRecord] = []

def create_record(
    student_id: int,
    first_name: str,
    second_name: str,
    age: int,
    sex: str,
) -> StudentRecord:
    if age < 0:
        raise ValueError("Поле age не может быть отрицательным.")
    if any(record[0] == student_id for record in Student):
        raise ValueError(f"Запись с id={student_id} уже существует.")
    new_record: StudentRecord = (
        student_id,
        first_name.strip(),
        second_name.strip(),
        age,
        sex.strip(),
    )
    Student.append(new_record)
    return new_record

def select_record(
    student_id: int | None = None,
    first_name: str | None = None,
    second_name: str | None = None,
    age: int | None = None,
    sex: str | None = None,
) -> list[StudentRecord]:
    if all(param is None for param in (student_id, first_name, second_name, age, sex)):
        return Student.copy()

    result: list[StudentRecord] = []
    for record in Student:
        if student_id is not None and record[0] != student_id:
            continue
        if first_name is not None and record[1] != first_name:
            continue
        if second_name is not None and record[2] != second_name:
            continue
        if age is not None and record[3] != age:
            continue
        if sex is not None and record[4] != sex:
            continue
        result.append(record)
    return result

def update_record(
    student_id: int,
    first_name: str | None = None,
    second_name: str | None = None,
    age: int | None = None,
    sex: str | None = None,
) -> StudentRecord:
    for i, record in enumerate(Student):
        if record[0] == student_id:
            updated_record = list(record)
            if first_name is not None:
                updated_record[1] = first_name.strip()
            if second_name is not None:
                updated_record[2] = second_name.strip()
            if age is not None:
                if age < 0:
                    raise ValueError("Поле age не может быть отрицательным.")
                updated_record[3] = age
            if sex is not None:
                updated_record[4] = sex.strip()
            Student[i] = tuple(updated_record)
            return Student[i]
    raise KeyError(f"Запись с id={student_id} не найдена.")

def delete_record(student_id: int) -> None:
    for i, record in enumerate(Student):
        if record[0] == student_id:
            del Student[i]
            return
    raise KeyError(f"Запись с id={student_id} не найдена.")
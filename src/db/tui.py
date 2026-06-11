from .backend.memory import StudentTable
from .backend.file_database import FileDatabase

class TUI:
    def __init__(self):
        print("Выберите тип базы данных:")
        print("1. In-memory")
        print("2. File (JSON)")
        choice = input("Ваш выбор: ")

        if choice == "2":
            self.db = FileDatabase()
            self.db_type = "файловая"
        else:
            self.db = StudentTable()
            self.db_type = "in-memory"

        self.current_table = None

    def run(self):
        while True:
            print(f"\n--- {self.db_type} БД ---")
            print("1. Создать таблицу")
            print("2. Добавить запись")
            print("3. Найти записи")
            print("0. Выход")

            cmd = input("Выберите действие: ")

            if cmd == "1":
                name = input("Имя таблицы: ")
                self.current_table = name
                if hasattr(self.db, 'create_table'):
                    self.db.create_table(name)
                else:
                    print("Таблица создана (in-memory)")
                print(f"Таблица '{name}' создана")

            elif cmd == "2":
                if not self.current_table:
                    print("Сначала создайте таблицу")
                    continue
                try:
                    sid = int(input("ID: "))
                    fname = input("Имя: ")
                    sname = input("Фамилия: ")
                    age = int(input("Возраст: "))
                    sex = input("Пол (M/F): ")
                    self.db.create_record(self.current_table, sid, fname, sname, age, sex)
                    print("Запись добавлена")
                except Exception as e:
                    print(f"Ошибка: {e}")

            elif cmd == "3":
                if not self.current_table:
                    print("Сначала создайте таблицу")
                    continue
                print("Фильтры (Enter = пропустить):")
                sid = input("ID: ")
                fname = input("Имя: ")
                sname = input("Фамилия: ")
                age = input("Возраст: ")
                sex = input("Пол: ")

                filters = {}
                if sid:
                    filters["student_id"] = int(sid)
                if fname:
                    filters["first_name"] = fname
                if sname:
                    filters["second_name"] = sname
                if age:
                    filters["age"] = int(age)
                if sex:
                    filters["sex"] = sex

                results = self.db.select_records(self.current_table, **filters)
                print("\nРезультаты:")
                for r in results:
                    print(r)

            elif cmd == "0":
                print("Выход.")
                break

def run():
    cli = TUI()
    cli.run()
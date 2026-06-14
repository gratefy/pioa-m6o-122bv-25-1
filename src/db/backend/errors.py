class StudentTableError(Exception):
    """Базовый класс для ошибок, связанных с таблицей Student."""
    pass

class InvalidAgeError(StudentTableError):
    """Ошибка, возникающая при попытке создать запись с некорректным возрастом."""
    pass

class DuplicateIDError(StudentTableError):
    """Ошибка, возникающая при попытке создать запись с уже существующим идентификатором."""
    pass

class DatabaseError(Exception):
    """Базовый класс для ошибок базы данных."""
    pass

class TableNotFoundError(DatabaseError):
    """Ошибка при обращении к несуществующей таблице."""
    pass

class TableAlreadyExistsError(DatabaseError):
    """Ошибка при попытке создать уже существующую таблицу."""
    pass

class InvalidStorageDataError(DatabaseError):
    """Ошибка при чтении повреждённого файла."""
    pass

class InvalidInputError(DatabaseError):
    """Ошибка при некорректном вводе пользователя."""
    pass
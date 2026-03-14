# Тут будуть знаходитись кастомні винятки програми та загальний декоратор input_error

class ValidationException(Exception):
    pass

def input_error(func):
    def wrapper(*args, **kwargs):
        # TODO: Реалізувати загальну обробку помилок (ValueError, KeyError, IndexError, ValidationException)
        pass
    return wrapper

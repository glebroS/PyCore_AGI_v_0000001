class ValidationException(Exception):
    pass


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationException as e:
            return f"Помилка валідації: {str(e)}"
        except ValueError as e:
            return f"Помилка вводу: {str(e)}"
        except KeyError:
            return "Помилка: Контакт не знайдено."
        except IndexError:
            return "Помилка: Недостатньо аргументів для команди."
        except Exception as e:
            return f"Невідома помилка: {str(e)}"
    return wrapper

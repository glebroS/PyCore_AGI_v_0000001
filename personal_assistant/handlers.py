# Тут будуть обробники команд консолі для роботи з контактами та нотатками
from .exceptions import input_error

@input_error
def add_contact(args, book):
    # TODO: Реалізувати додавання контакту
    pass

@input_error
def change_contact(args, book):
    # TODO: Реалізувати редагування номера телефону
    pass

@input_error
def add_note_handler(args, notebook):
    # TODO: Реалізувати додавання нотатки
    pass

# ... Інші обробники ...

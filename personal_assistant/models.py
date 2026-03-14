# Тут будуть класи даних для контактів (Phone, Name, Birthday, Email, Address, Record, AddressBook)
# та концепцій нотаток (Note, NoteBook)

from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    # TODO: Додати валідацію для 10 цифр
    pass

# ... Інші класи ...

class Record:
    def __init__(self, name):
        self.name = Name(name)
        # TODO: Додати поля для phones, emails, address, birthday
        
class AddressBook(UserDict):
    # TODO: Реалізувати методи пошуку, додавання, видалення, пошук найближчих днів народження
    pass

class NoteBook(UserDict):
    # TODO: Реалiзувати зберiгання нотаток та тегiв
    pass

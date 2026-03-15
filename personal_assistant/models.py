import re
from collections import UserDict
from datetime import datetime, timedelta
from personal_assistant.exceptions import ValidationException


class Field:
    """Базовий клас для полів запису контакту."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """Клас для зберігання імені контакту."""
    pass


class Phone(Field):
    """Клас для зберігання номера телефону з валідацією (10 цифр)."""

    def __init__(self, value):
        value = str(value)
        if not value.isdigit() or len(value) != 10:
            raise ValidationException(f"Номер телефону повинен мати 10 цифр. Отримано: {value}")
        super().__init__(value)


class Email(Field):
    """Клас для зберігання email з валідацією формату."""

    def __init__(self, value):
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(pattern, value):
            raise ValidationException(f"Невірний формат email. Отримано: {value}")
        super().__init__(value)


class Address(Field):
    """Клас для зберігання адреси контакту."""
    pass


class Birthday(Field):
    """Клас для зберігання дня народження з валідацією формату DD.MM.YYYY."""

    def __init__(self, value):
        try:
            birthday_obj = datetime.strptime(value, "%d.%m.%Y")
            if birthday_obj > datetime.now():
                raise ValidationException("Дата народження не може бути в майбутньому.")
            self.value = birthday_obj.strftime("%d.%m.%Y")
        except ValueError:
            raise ValidationException("Невірний формат дати. Використовуйте DD.MM.YYYY")

    def __str__(self):
        return self.value


class Record:
    """Клас для зберігання інформації про контакт: ім'я, телефони, email, адреса, день народження."""

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.emails = []
        self.address = None
        self.birthday = None

    def add_phone(self, phone):
        """Додає номер телефону до контакту."""
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        """Видаляє номер телефону з контакту."""
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        """Змінює існуючий номер телефону на новий."""
        found = False
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[i] = Phone(new_phone)
                found = True
                break
        if not found:
            raise ValidationException(f"Телефон {old_phone} не знайдено.")

    def find_phone(self, phone):
        """Шукає телефон у списку та повертає об'єкт Phone або None."""
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_email(self, email):
        """Додає email до контакту."""
        self.emails.append(Email(email))

    def remove_email(self, email):
        """Видаляє email з контакту."""
        self.emails = [e for e in self.emails if e.value != email]

    def edit_email(self, old_email, new_email):
        """Змінює існуючий email на новий."""
        found = False
        for i, email in enumerate(self.emails):
            if email.value == old_email:
                self.emails[i] = Email(new_email)
                found = True
                break
        if not found:
            raise ValidationException(f"Email {old_email} не знайдено.")

    def add_address(self, address):
        """Додає адресу до контакту."""
        self.address = Address(address)

    def add_birthday(self, birthday):
        """Додає день народження до контакту."""
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones_str = "; ".join(p.value for p in self.phones) if self.phones else "немає"
        emails_str = "; ".join(e.value for e in self.emails) if self.emails else "немає"
        address_str = self.address.value if self.address else "немає"
        birthday_str = self.birthday.value if self.birthday else "немає"

        return (f"Контакт: {self.name.value} | Телефони: {phones_str} | "
                f"Email: {emails_str} | Адреса: {address_str} | День народження: {birthday_str}")


class AddressBook(UserDict):
    """Клас для зберігання та управління колекцією контактів."""

    def add_record(self, record):
        """Додає запис контакту до книги."""
        self.data[record.name.value] = record

    def find(self, name):
        """Знаходить контакт за іменем. Повертає Record або None."""
        return self.data.get(name)

    def delete(self, name):
        """Видаляє контакт за іменем."""
        if name in self.data:
            del self.data[name]
            return f"Контакт {name} успішно видалено."
        else:
            raise KeyError(f"Контакт {name} не знайдено.")

    def get_all_contacts(self):
        """Повертає список усіх контактів."""
        return list(self.data.values())

    def get_upcoming_birthdays(self, days=7):
        """Повертає список контактів з днями народження в найближчі N днів."""
        upcoming = []
        today = datetime.now()
        for i in range(days):
            check_date = today + timedelta(days=i)
            for record in self.data.values():
                if record.birthday:
                    birthday_date = datetime.strptime(record.birthday.value, "%d.%m.%Y")
                    if (birthday_date.day == check_date.day and
                            birthday_date.month == check_date.month):
                        upcoming.append({
                            "name": record.name.value,
                            "birthday": record.birthday.value,
                            "congratulation_date": check_date.strftime("%d.%m.%Y")
                        })
        return upcoming

    def search_contacts(self, query):
        """Пошук контактів за іменем, телефоном або email."""
        results = []
        for record in self.data.values():
            if query.lower() in record.name.value.lower():
                results.append(record)
                continue

            phone_match = False
            for phone in record.phones:
                if query in phone.value:
                    results.append(record)
                    phone_match = True
                    break
            if phone_match:
                continue

            for email in record.emails:
                if query.lower() in email.value.lower():
                    results.append(record)
                    break

        return results

    def __getstate__(self):
        return self.data

    def __setstate__(self, state):
        self.data = state


class Note:
    """Клас для зберігання нотатки з заголовком, текстом та тегами."""

    def __init__(self, title, content=""):
        self.title = title
        self.content = content
        self.tags = set()

    def edit_content(self, new_content):
        """Змінює текст нотатки."""
        self.content = new_content

    def add_tag(self, tag):
        """Додає тег до нотатки."""
        self.tags.add(tag)

    def remove_tag(self, tag):
        """Видаляє тег з нотатки."""
        if tag in self.tags:
            self.tags.remove(tag)
        else:
            raise ValidationException(f"Тег '{tag}' не знайдено в нотатці '{self.title}'.")

    def __str__(self):
        tags_str = ", ".join(self.tags) if self.tags else "немає"
        return f"Нотатка: {self.title}\nТекст: {self.content}\nТеги: [{tags_str}]"


class NoteBook(UserDict):
    """Клас для зберігання та управління колекцією нотаток."""

    def add_note(self, note):
        """Додає нотатку до книги нотаток."""
        if note.title in self.data:
            raise ValidationException(f"Нотатка з назвою '{note.title}' вже існує.")
        self.data[note.title] = note

    def find_note(self, title):
        """Знаходить нотатку за заголовком. Повертає Note або None."""
        return self.data.get(title)

    def delete_note(self, title):
        """Видаляє нотатку за заголовком."""
        if title in self.data:
            del self.data[title]
            return f"Нотатку '{title}' успішно видалено."
        raise KeyError(f"Нотатку '{title}' не знайдено.")

    def get_all_notes(self):
        """Повертає список усіх нотаток."""
        return list(self.data.values())

    def search_by_text(self, keyword):
        """Пошук нотаток за ключовим словом у заголовку або тексті."""
        results = []
        for note in self.data.values():
            if keyword.lower() in note.title.lower() or keyword.lower() in note.content.lower():
                results.append(note)
        return results

    def search_by_tag(self, tag):
        """Пошук нотаток за тегом. Результати відсортовані за заголовком."""
        results = []
        for note in self.data.values():
            if tag in note.tags:
                results.append(note)
        return sorted(results, key=lambda n: n.title)

    def __getstate__(self):
        return self.data

    def __setstate__(self, state):
        self.data = state
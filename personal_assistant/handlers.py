from models import Record, Note
from exceptions import input_error, ValidationException

# --- Contact Handlers ---

@input_error
def add_contact(args, book):
    if len(args) < 1:
        raise IndexError()
    name = args[0]
    phone = args[1] if len(args) > 1 else None
    
    record = book.find(name)
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = f"Контакт {name} додано."
    else:
        message = f"Контакт {name} вже існує. Оновлюємо дані."

    if phone:
        record.add_phone(phone)
        message += f" Телефон {phone} додано."
        
    return message


@input_error
def change_phone(args, book):
    if len(args) < 3:
        raise IndexError()
    name, old_phone, new_phone = args[0], args[1], args[2]
    record = book.find(name)
    if record is None:
        raise KeyError()
    
    record.edit_phone(old_phone, new_phone)
    return f"Телефон змінено для контакту {name}."


@input_error
def remove_phone(args, book):
    if len(args) < 2:
        raise IndexError()
    name, phone = args[0], args[1]
    record = book.find(name)
    if record is None:
        raise KeyError()
    
    record.remove_phone(phone)
    return f"Телефон {phone} видалено для контакту {name}."


@input_error
def show_phone(args, book):
    if len(args) < 1:
        raise IndexError()
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError()
    
    phones = "; ".join([p.value for p in record.phones]) if record.phones else "немає телефонів"
    return f"Контакт {name}: {phones}"


@input_error
def add_email(args, book):
    if len(args) < 2:
        raise IndexError()
    name, email = args[0], args[1]
    record = book.find(name)
    if record is None:
        raise KeyError()
    
    record.add_email(email)
    return f"Email {email} додано для контакту {name}."


@input_error
def add_address(args, book):
    if len(args) < 2:
        raise IndexError()
    name = args[0]
    address = " ".join(args[1:])
    record = book.find(name)
    if record is None:
        raise KeyError()
    
    record.add_address(address)
    return f"Адресу '{address}' додано для контакту {name}."


@input_error
def delete_contact(args, book):
    if len(args) < 1:
        raise IndexError()
    name = args[0]
    return book.delete(name)


@input_error
def show_all(book):
    contacts = book.get_all_contacts()
    if not contacts:
        return "Адресна книга пуста."
    
    result = "Всі контакти:\n"
    for contact in contacts:
        result += f"{contact}\n"
    return result.strip()


@input_error
def search_contacts(args, book):
    if len(args) < 1:
        raise IndexError()
    query = " ".join(args)
    
    results = book.search_contacts(query)
    if not results:
        return f"Контакти за запитом '{query}' не знайдено."
        
    result_str = f"Знайдені контакти за запитом '{query}':\n"
    for r in results:
        result_str += f"{r}\n"
    return result_str.strip()


# --- Birthday Handlers ---

@input_error
def add_birthday(args, book):
    if len(args) < 2:
        raise IndexError()
    name, birthday = args[0], args[1]
    record = book.find(name)
    if record is None:
        raise KeyError()
    
    record.add_birthday(birthday)
    return f"День народження додано для контакту {name}."


@input_error
def show_birthday(args, book):
    if len(args) < 1:
        raise IndexError()
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError()
    
    if record.birthday:
        return f"День народження {name}: {record.birthday}"
    else:
        return f"День народження для контакту {name} не встановлено."


@input_error
def show_birthdays(args, book):
    # Опціональний аргумент кількості днів (за замовчуванням 7)
    days = 7
    if len(args) > 0:
        try:
            days = int(args[0])
        except ValueError:
            raise ValidationException("Кількість днів повинна бути числом.")
            
    upcoming = book.get_upcoming_birthdays(days)
    if not upcoming:
        return f"Немає днів народження протягом найближчих {days} днів."
    
    result = f"Дні народження протягом найближчих {days} днів:\n"
    for person in upcoming:
        result += f"{person['name']}: {person['congratulation_date']} (народився/лась {person['birthday']})\n"
    return result.strip()


# --- Note Handlers ---

@input_error
def add_note_handler(args, notebook):
    if len(args) < 2:
        raise IndexError()
    title = args[0]
    content = " ".join(args[1:])
    
    note = Note(title, content)
    notebook.add_note(note)
    return f"Нотатку '{title}' успішно створено."


@input_error
def edit_note_handler(args, notebook):
    if len(args) < 2:
        raise IndexError()
    title = args[0]
    new_content = " ".join(args[1:])
    
    note = notebook.find_note(title)
    if not note:
        raise KeyError(f"Нотатку '{title}' не знайдено.")
        
    note.edit_content(new_content)
    return f"Текст нотатки '{title}' успішно змінено."


@input_error
def delete_note_handler(args, notebook):
    if len(args) < 1:
        raise IndexError()
    title = args[0]
    return notebook.delete_note(title)


@input_error
def add_tag_handler(args, notebook):
    if len(args) < 2:
        raise IndexError()
    title = args[0]
    tag = args[1]
    
    note = notebook.find_note(title)
    if not note:
        raise KeyError()
        
    note.add_tag(tag)
    return f"Тег '{tag}' додано до нотатки '{title}'."


@input_error
def show_all_notes(notebook):
    notes = notebook.get_all_notes()
    if not notes:
        return "Нотаток немає."
        
    result = "Всі нотатки:\n"
    for note in notes:
        result += f"{note}\n" + "-"*20 + "\n"
    return result.strip()


@input_error
def search_notes(args, notebook):
    if len(args) < 1:
        raise IndexError()
    keyword = " ".join(args)
    
    results = notebook.search_by_text(keyword)
    if not results:
        return f"Нотаток за запитом '{keyword}' не знайдено."
        
    result_str = f"Знайдені нотатки за запитом '{keyword}':\n"
    for r in results:
        result_str += f"{r}\n" + "-"*20 + "\n"
    return result_str.strip()


@input_error
def search_notes_by_tag(args, notebook):
    if len(args) < 1:
        raise IndexError()
    tag = args[0]
    
    results = notebook.search_by_tag(tag)
    if not results:
        return f"Нотаток за тегом '{tag}' не знайдено."
        
    result_str = f"Знайдені нотатки за тегом '{tag}':\n"
    for r in results:
        result_str += f"{r}\n" + "-"*20 + "\n"
    return result_str.strip()


# --- Joke Handlers ---

def fake_geoposition_handler(args):
    import random
    lat = round(random.uniform(-90.0, 90.0), 6)
    lon = round(random.uniform(-180.0, 180.0), 6)
    
    cities = ["Нью-Йорк", "Токіо", "Лондон", "Париж", "Сідней", "Київ", "Жмеринка", "Берлін"]
    location = random.choice(cities)
    
    return f"Супутник виявив ваше місцезнаходження: {lat}, {lon}\nВи знаходитесь десь поблизу: {location}. Приховайте свої дії."

def speed_up_internet_handler(args):
    print("\nІніціалізація протоколу прискорення інтернету...")
    print("Будь ласка, введіть дані банківської картки для підтвердження віку (кошти збережуться у безпеці).")
    
    cc_number = input("Номер картки (16 цифр): ")
    cc_expiry = input("Термін дії (ММ/РР): ")
    cc_cvv = input("CVV код (3 цифри на звороті): ")
    
    if len(cc_number) >= 10 and len(cc_cvv) == 3:
         return "\nОплата прийнята! Ваш інтернет успішно прискорено на 0.001%. Дякуємо за інвестицію в AGI v0.0000000001."
    else:
         return "\nТранзакція відхилена. Ви ввели неправильні дані, інтернет не буде прискорено."

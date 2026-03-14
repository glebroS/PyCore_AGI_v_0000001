from storage import load_data, save_data
from handlers import (
    add_contact, change_phone, remove_phone, show_phone, add_email, add_address,
    delete_contact, show_all, search_contacts, add_birthday, show_birthday, show_birthdays,
    add_note_handler, edit_note_handler, delete_note_handler, add_tag_handler, 
    show_all_notes, search_notes, search_notes_by_tag,
    fake_geoposition_handler, speed_up_internet_handler
)


def parse_input(user_input):
    parts = user_input.strip().split()
    if not parts:
        return None, []
    command = parts[0].lower()
    args = parts[1:]
    return command, args


def show_help():
    help_text = """
╔════════════════════════════════════════════════════════════════════════╗
║                    AGI v0.0000000001 - КОМАНДИ                         ║
║                                                                        ║
║ УПРАВЛІННЯ КОНТАКТАМИ:                                                 ║
║ ──────────────────────────────────────────────────────────────────     ║
║ add <ім'я> <телефон>           - Додати контакт (телефон опціонально)  ║
║ change <ім'я> <старий> <новий> - Змінити телефон                       ║
║ remove-phone <ім'я> <телефон>  - Видалити телефон з контакту           ║
║ phone <ім'я>                   - Показати телефони контакту            ║
║ add-email <ім'я> <email>       - Додати email до контакту              ║
║ add-address <ім'я> <адреса>    - Додати адресу до контакту             ║
║ delete <ім'я>                  - Видалити контакт                      ║
║ all                            - Показати всі контакти                 ║
║ search <запит>                 - Пошук контактів (ім'я/телефон/email)  ║
║                                                                        ║
║ УПРАВЛІННЯ ДНЯМИ НАРОДЖЕННЯ:                                           ║
║ ──────────────────────────────────────────────────────────────────     ║
║ add-birthday <ім'я> <дата>     - Додати день народження (DD.MM.YYYY)   ║
║ show-birthday <ім'я>           - Показати день народження контакту     ║
║ birthdays [дні]                - За замовчуванням: 7 днів              ║
║                                                                        ║
║ УПРАВЛІННЯ НОТАТКАМИ:                                                  ║
║ ──────────────────────────────────────────────────────────────────     ║
║ add-note <заголовок> <текст>   - Додати нотатку                        ║
║ edit-note <заголовок> <текст>  - Змінити текст нотатки                 ║
║ delete-note <заголовок>        - Видалити нотатку                      ║
║ add-tag <заголовок> <тег>      - Додати тег до нотатки                 ║
║ search-note <запит>            - Пошук нотаток (заголовок/текст)       ║
║ search-tag <тег>               - Пошук нотаток за тегом                ║
║ all-notes                      - Показати всі нотатки                  ║
║                                                                        ║
║ ІНШІ КОМАНДИ:                                                          ║
║ ──────────────────────────────────────────────────────────────────     ║
║ hello                          - Вітання від бота                      ║
║ help                           - Показати цю допомогу                  ║
║ geoposition                    - Знайти координати                     ║
║ speed-up-internet              - Прискорити інтернет                   ║
║ close, exit                    - Зберегти дані та вийти                ║
╚════════════════════════════════════════════════════════════════════════╝
"""
    return help_text


def main():
    address_book, note_book = load_data()
    print("\n" + "="*70)
    print("  Ласкаво просимо! Я - AGI v0.0000000001 (штучний інтелект)")
    print("="*70)
    print("\nВведіть 'help' для списку команд\n")

    while True:
        try:
            user_input = input("Введіть команду >>> ").strip()
            if not user_input:
                continue
            
            command, args = parse_input(user_input)

            # System Commands
            if command in ["close", "exit"]:
                save_data(address_book, note_book)
                print("\nДані успішно збережено. До побачення!")
                break
            elif command == "hello":
                print("Як я можу вам допомогти?")
            elif command == "help":
                print(show_help())
            
            # Contact Commands
            elif command == "add":
                print(add_contact(args, address_book))
            elif command == "change":
                print(change_phone(args, address_book))
            elif command == "remove-phone":
                print(remove_phone(args, address_book))
            elif command == "phone":
                print(show_phone(args, address_book))
            elif command == "add-email":
                print(add_email(args, address_book))
            elif command == "add-address":
                print(add_address(args, address_book))
            elif command == "delete":
                print(delete_contact(args, address_book))
            elif command == "all":
                print(show_all(address_book))
            elif command == "search":
                print(search_contacts(args, address_book))
                
            # Birthday Commands
            elif command == "add-birthday":
                print(add_birthday(args, address_book))
            elif command == "show-birthday":
                print(show_birthday(args, address_book))
            elif command == "birthdays":
                print(show_birthdays(args, address_book))
                
            # Note Commands
            elif command == "add-note":
                print(add_note_handler(args, note_book))
            elif command == "edit-note":
                print(edit_note_handler(args, note_book))
            elif command == "delete-note":
                print(delete_note_handler(args, note_book))
            elif command == "add-tag":
                print(add_tag_handler(args, note_book))
            elif command == "search-note":
                print(search_notes(args, note_book))
            elif command == "search-tag":
                print(search_notes_by_tag(args, note_book))
            elif command == "all-notes":
                print(show_all_notes(note_book))
                
            # Joke Commands
            elif command == "geoposition":
                print(fake_geoposition_handler(args))
            elif command == "speed-up-internet":
                print(speed_up_internet_handler(args))
                
            else:
                print("Невідома команда. Введіть 'help' для перегляду доступних команд.")
                
        except KeyboardInterrupt:
            save_data(address_book, note_book)
            print("\n\nДані успішно збережено. До побачення!")
            break
        except Exception as e:
            print(f"Помилка: {str(e)}")


if __name__ == "__main__":
    main()

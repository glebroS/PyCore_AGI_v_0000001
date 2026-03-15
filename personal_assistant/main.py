from personal_assistant.storage import load_data, save_data
from personal_assistant.handlers import (
    add_contact, change_phone, remove_phone, show_phone, add_email, remove_email, edit_email, add_address,
    remove_address, delete_contact, edit_contact_name, show_all, search_contacts, add_birthday, show_birthday, show_birthdays,
    add_note_handler, edit_note_handler, delete_note_handler, show_note_handler, add_tag_handler, remove_tag_handler,
    show_all_notes, search_notes, search_notes_by_tag,
    fake_geoposition_handler, speed_up_internet_handler
)

import shlex
from colorama import init, Fore, Style
from difflib import get_close_matches

init(autoreset=True)

ALL_COMMANDS = [
    "add", "change", "remove-phone", "phone", "add-email", "remove-email",
    "edit-email", "add-address", "remove-address", "edit-name", "delete",
    "all", "search", "add-birthday", "show-birthday", "birthdays",
    "add-note", "show-note", "edit-note", "delete-note", "add-tag",
    "remove-tag", "search-note", "search-tag", "all-notes",
    "hello", "help", "geoposition", "speed-up-internet", "close", "exit"
]

def parse_input(user_input):
    try:
        parts = shlex.split(user_input.strip())
    except ValueError:
        parts = user_input.strip().split()
    if not parts:
        return None, []
    command = parts[0].lower()
    args = parts[1:]
    return command, args


def ok(msg):
    return Fore.GREEN + msg + Style.RESET_ALL


def err(msg):
    return Fore.RED + msg + Style.RESET_ALL


def info(msg):
    return Fore.CYAN + msg + Style.RESET_ALL


def show_help():
    help_text = Fore.CYAN + """
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
║ remove-email <ім'я> <email>    - Видалити email контакту               ║
║ edit-email <ім'я> <старий> <новий> - Змінити email контакту            ║
║ add-address <ім'я> <адреса>    - Додати адресу до контакту             ║
║ remove-address <ім'я>          - Видалити адресу контакту              ║
║ edit-name <старе> <нове>       - Змінити ім'я контакту                 ║
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
║ add-note "<заголовок>" <текст> - Додати нотатку                        ║
║ show-note <заголовок>          - Показати одну нотатку                 ║
║ edit-note "<заголовок>" <текст>- Змінити текст нотатки                 ║
║ delete-note <заголовок>        - Видалити нотатку                      ║
║ add-tag <заголовок> <тег>      - Додати тег до нотатки                 ║
║ remove-tag <заголовок> <тег>   - Видалити тег з нотатки               ║
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
""" + Style.RESET_ALL
    return help_text


def main():
    address_book, note_book = load_data()
    print(Fore.CYAN + "\n" + "="*70)
    print("  Ласкаво просимо! Я - AGI v0.0000000001 (штучний інтелект)")
    print("="*70 + Style.RESET_ALL)
    print(Fore.YELLOW + "\nВведіть 'help' для списку команд\n" + Style.RESET_ALL)

    while True:
        try:
            user_input = input(Fore.YELLOW + "Введіть команду >>> " + Style.RESET_ALL).strip()
            if not user_input:
                continue
            
            command, args = parse_input(user_input)

            # System Commands
            if command in ["close", "exit"]:
                save_data(address_book, note_book)
                print(ok("\nДані успішно збережено. До побачення!"))
                break
            elif command == "hello":
                print(info("Як я можу вам допомогти?"))
            elif command == "help":
                print(show_help())
            
            # Contact Commands
            elif command == "add":
                print(ok(add_contact(args, address_book)))
            elif command == "change":
                print(ok(change_phone(args, address_book)))
            elif command == "remove-phone":
                print(ok(remove_phone(args, address_book)))
            elif command == "phone":
                print(info(show_phone(args, address_book)))
            elif command == "add-email":
                print(ok(add_email(args, address_book)))
            elif command == "remove-email":
                print(ok(remove_email(args, address_book)))
            elif command == "edit-email":
                print(ok(edit_email(args, address_book)))
            elif command == "add-address":
                print(ok(add_address(args, address_book)))
            elif command == "remove-address":
                print(ok(remove_address(args, address_book)))
            elif command == "edit-name":
                print(ok(edit_contact_name(args, address_book)))
            elif command == "delete":
                print(ok(delete_contact(args, address_book)))
            elif command == "all":
                print(info(show_all(address_book)))
            elif command == "search":
                print(info(search_contacts(args, address_book)))
                
            # Birthday Commands
            elif command == "add-birthday":
                print(ok(add_birthday(args, address_book)))
            elif command == "show-birthday":
                print(info(show_birthday(args, address_book)))
            elif command == "birthdays":
                print(info(show_birthdays(args, address_book)))
                
            # Note Commands
            elif command == "add-note":
                print(ok(add_note_handler(args, note_book)))
            elif command == "show-note":
                print(info(show_note_handler(args, note_book)))
            elif command == "edit-note":
                print(ok(edit_note_handler(args, note_book)))
            elif command == "delete-note":
                print(ok(delete_note_handler(args, note_book)))
            elif command == "add-tag":
                print(ok(add_tag_handler(args, note_book)))
            elif command == "remove-tag":
                print(ok(remove_tag_handler(args, note_book)))
            elif command == "search-note":
                print(info(search_notes(args, note_book)))
            elif command == "search-tag":
                print(info(search_notes_by_tag(args, note_book)))
            elif command == "all-notes":
                print(info(show_all_notes(note_book)))
                
            # Joke Commands
            elif command == "geoposition":
                print(info(fake_geoposition_handler(args)))
            elif command == "speed-up-internet":
                print(fake_geoposition_handler(args))
                
            else:
                suggestion = get_close_matches(command, ALL_COMMANDS, n=1, cutoff=0.5)
                if suggestion:
                    print(err(f"Невідома команда '{command}'. Можливо, ви мали на увазі: '{suggestion[0]}'?"))
                else:
                    print(err(f"Невідома команда '{command}'. Введіть 'help' для перегляду доступних команд."))
                
        except KeyboardInterrupt:
            save_data(address_book, note_book)
            print(ok("\n\nДані успішно збережено. До побачення!"))
            break
        except Exception as e:
            print(err(f"Помилка: {str(e)}"))


if __name__ == "__main__":
    main()
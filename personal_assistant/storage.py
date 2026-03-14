import pickle
import os
from pathlib import Path
from personal_assistant.models import AddressBook, NoteBook

# Get user home directory to save files
USER_HOME = str(Path.home())
APP_DIR = os.path.join(USER_HOME, "personal_assistant_data")

if not os.path.exists(APP_DIR):
    os.makedirs(APP_DIR)

CONTACTS_FILE = os.path.join(APP_DIR, "addressbook.pkl")
NOTES_FILE = os.path.join(APP_DIR, "notebook.pkl")


def save_data(address_book, note_book):
    with open(CONTACTS_FILE, "wb") as f:
        pickle.dump(address_book, f)
        
    with open(NOTES_FILE, "wb") as f:
        pickle.dump(note_book, f)


def load_data():
    address_book = AddressBook()
    note_book = NoteBook()

    if os.path.exists(CONTACTS_FILE):
        try:
            with open(CONTACTS_FILE, "rb") as f:
                address_book = pickle.load(f)
        except Exception:
            pass

    if os.path.exists(NOTES_FILE):
        try:
            with open(NOTES_FILE, "rb") as f:
                note_book = pickle.load(f)
        except Exception:
            pass

    return address_book, note_book

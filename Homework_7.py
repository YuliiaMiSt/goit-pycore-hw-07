#Task_1#
from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.validate(value)

    def validate(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Invalid phone number format")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                break

    def find_phone(self, phone):
        return any(p.value == phone for p in self.phones)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def days_to_birthday(self):
        if not self.birthday:
            return None
        today = datetime.now()
        next_birthday = self.birthday.value.replace(year=today.year)
        if next_birthday < today:
            next_birthday = next_birthday.replace(year=today.year + 1)
        return (next_birthday - today).days


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find_records(self, name):
        return [record for record in self.data.values() if record.name.value == name]

    def remove_records(self, name):
        for record in self.find_records(name):
            del self.data[record.name.value]

    
    from datetime import datetime, timedelta
    def get_upcoming_birthdays(users):
    today = datetime.today().date()
 
    upcoming_birthdays = []

    for user in users:
        birthday = datetime.strptime(user["birthday"], "%Y.%m.%d").date()
        if birthday < today:
            birthday = birthday.replace(year=today.year + 1)
        days_until_birthday = (birthday - today).days
 
        if 0 <= days_until_birthday <= 7:
            if birthday.weekday() >= 5:
                next_monday = today + timedelta(days=(7 - today.weekday()) + 1)
                congratulation_date = next_monday.strftime("%Y.%m.%d")
            else:
                congratulation_date = birthday.strftime("%Y.%m.%d")
            upcoming_birthday = {"name": user["name"], "congratulation_date": congratulation_date}
            upcoming_birthdays.append(upcoming_birthday)
 
    return upcoming_birthdays


#Task_2#
import re
from datetime import datetime, timedelta

class Field:
    pass

class Name(Field):
    def __init__(self, value):
        self.value = value

class Phone(Field):
    def __init__(self, value):
        if re.match(r'^\d{10}$', value):
            self.value = value
        else:
            raise ValueError("Invalid phone number format. Use 10 digits.")

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def delete_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def change_phone(self, old_phone, new_phone):
        self.delete_phone(old_phone)
        self.add_phone(new_phone)

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

class AddressBook:
    def __init__(self):
        self.records = {}

    def add_record(self, record):
        self.records[record.name.value] = record

    def find(self, name):
        return self.records.get(name, None)

    def get_all_records(self):
        return self.records.values()

    def get_upcoming_birthdays(self, days=7):
        upcoming = []
        today = datetime.now().date()
        for record in self.records.values():
            if record.birthday:
                bday_this_year = record.birthday.value.replace(year=today.year).date()
                if today <= bday_this_year <= (today + timedelta(days=days)):
                    upcoming.append(record)
        return upcoming

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError) as e:
            return str(e)
    return inner

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_contact(args, book):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")
    record.change_phone(old_phone, new_phone)
    return "Contact phone updated."

@input_error
def find_contact(args, book):
    name, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")
    return f"Name: {record.name.value}, Phones: {', '.join(phone.value for phone in record.phones)}"

@input_error
def add_birthday(args, book):
    name, birthday, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")
    record.add_birthday(birthday)
    return "Birthday added."

@input_error
def show_birthday(args, book):
    name, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")
    if record.birthday is None:
        return "Birthday not set."
    return f"Birthday: {record.birthday.value.strftime('%d.%m.%Y')}"

@input_error
def birthdays(args, book):
    upcoming_birthdays = book.get_upcoming_birthdays()
    if not upcoming_birthdays:
        return "No upcoming birthdays."
    result = []
    for record in upcoming_birthdays:
        result.append(f"{record.name.value}: {record.birthday.value.strftime('%d.%m.%Y')}")
    return "\n".join(result)

def parse_input(user_input):
    return user_input.split()

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(find_contact(args, book))

        elif command == "all":
            for record in book.get_all_records():
                phones = ', '.join(phone.value for phone in record.phones)
                birthday = record.birthday.value.strftime('%d.%m.%Y') if record.birthday else "N/A"
                print(f"Name: {record.name.value}, Phones: {phones}, Birthday: {birthday}")

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")
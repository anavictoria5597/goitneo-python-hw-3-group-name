from datetime import datetime, timedelta
from collections import defaultdict

class AddressBook:
    def __init__(self):
        #empty dictionary for contacts
        self.contacts = {}

    def add_contact(self, name, phone):
    #add contact details and check is the name already exists
        if name in self.contacts:
            return f"Contact '{name}' already exists."
        else:
            self.contacts[name] = {"phone": phone, "birthday": None}
            return f"Contact '{name}' successfully added."

    def update_contact(self, name, phone):
    #update an existing contact
        if name in self.contacts:
            self.contacts[name]["phone"] = phone
            return f"Phone number updated for contact '{name}'."
        else:
            return f"Contact '{name}' does not exist."

    def show_phone(self, name):
    #return the contact details if the contact exists
        if name in self.contacts:
            return f"Phone number for contact '{name}': {self.contacts[name]['phone']}"
        else:
            return f"Contact '{name}' does not exist."

    def show_all(self):
    #return all of the contacts stored
        return self.contacts

    def add_birthday(self, name, birth_date):
    #adds the birthdate to an existing contact 
        if name in self.contacts:
            self.contacts[name]["birthday"] = birth_date
            return f"Birthday added for contact '{name}'."
        else:
            return f"Contact '{name}' does not exist."

    def show_birthday(self, name):
    #returns the birthday for an existing contact
        if name in self.contacts and self.contacts[name]["birthday"]:
            return f"Birthday for contact '{name}': {self.contacts[name]['birthday']}"
        else:
            return f"No birthday found for contact '{name}'."

    def get_birthdays_per_week(self):
        birthday_per_week = defaultdict(list)
        current_date = datetime.today().date()
        next_week = current_date + timedelta(days=7)

        for name, info in self.contacts.items():
            if info["birthday"]:
                birth_date = datetime.strptime(info["birthday"], '%d.%m.%Y').date()
                birth_date_this_year = birth_date.replace(year=current_date.year)

                if birth_date_this_year < current_date:
                    birth_date_this_year = birth_date.replace(year=current_date.year + 1)

                delta_days = (birth_date_this_year - current_date).days

                if 0 <= delta_days < 7:
                    bday = birth_date_this_year.strftime('%A')
                    if bday == "Saturday" or bday == "Sunday":
                        bday = "Monday"
                    birthday_per_week[bday].append(name)

        return birthday_per_week

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Please provide correct input."
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Insufficient arguments provided."

    return inner

@input_error
def parse_input(user_input):
    parts = user_input.split()
    cmd = parts[0].strip().lower()
    args = parts[1:]
    return cmd, args

def main():
    address_book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Goodbye!")
            break
        elif command == "hello":
            print("Hello! How can I assist you today?")
        elif command == "add":
            if len(args) != 2:
                print("Please provide both name and phone number.")
            else:
                name, phone = args
                print(address_book.add_contact(name, phone))
        elif command == "update":
            if len(args) != 2:
                print("Please provide both name and new phone number.")
            else:
                name, phone = args
                print(address_book.update_contact(name, phone))
        elif command == "phone":
            if len(args) != 1:
                print("Please provide the name of the contact.")
            else:
                name = args[0]
                print(address_book.show_phone(name))
        elif command == "all":
            print(address_book.show_all())
        elif command == "add-birthday":
            if len(args) != 2:
                print("Please provide both name and birthday in DD.MM.YYYY format.")
            else:
                name, birth_date = args
                print(address_book.add_birthday(name, birth_date))
        elif command == "show-birthday":
            if len(args) != 1:
                print("Please provide the name of the contact.")
            else:
                name = args[0]
                print(address_book.show_birthday(name))
        elif command == "birthdays":
            birthdays = address_book.get_birthdays_per_week()
            if birthdays:
                for day, contacts in birthdays.items():
                    print(f"{day}: {', '.join(contacts)}")
            else:
                print("No birthdays in the next week.")
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
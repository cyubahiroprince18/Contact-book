import re
import json


class Contact:
    def __init__(self, id, name, phone, email):
        self.id = id
        self.name = name
        self.phone = phone
        self.email = email

    def __str__(self):
        return f"{self.id}. {self.name} - {self.phone} - {self.email}"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email
        }


# --- Storage ---
contacts = {}
next_id = 1


# --- Validation ---
def validate_phone(phone):
    pattern = r"^\d{3}-\d{3}-\d{4}$"
    if re.match(pattern, phone):
        return True
    else:
        return False


def validate_email(email):
    pattern = r"^[a-zA-Z0-9._]+@[a-zA-Z0-9.]+\.[a-zA-Z]+$"
    if re.match(pattern, email):
        return True
    else:
        return False


# --- Add a new contact (with validation) ---
def add_contact(name, phone, email):
    global next_id
    if not validate_phone(phone):
        print(f"Phone number {phone} is invalid, must be in format XXX-XXX-XXXX")
        return False
    if not validate_email(email):
        print(f"Email {email} is invalid, must be in format name@domain.com")
        return False
    new_contact = Contact(next_id, name, phone, email)
    contacts[next_id] = new_contact
    next_id += 1
    return True


# --- Search for a contact by name (case-insensitive, whitespace-tolerant) ---
def search_contact(name):
    for contact in contacts.values():
        if contact.name.strip().lower() == name.strip().lower():
            return contact
    print(f"{name} not found")
    return None


# --- Update an existing contact by id ---
def update_contact(id, name=None, phone=None, email=None):
    if id not in contacts:
        print(f"{id} not found")
        return False

    contact = contacts[id]

    if name is not None:
        contact.name = name
    if phone is not None:
        contact.phone = phone
    if email is not None:
        contact.email = email

    return True


# --- Delete a contact by id ---
def delete_contact(id):
    if id in contacts:
        del contacts[id]
        return True
    print(f"{id} not found")
    return False


# --- Save all contacts to a JSON file ---
def save_contacts():
    data = {}
    for id, contact in contacts.items():
        data[id] = contact.to_dict()
    with open("contacts.json", "w") as file:
        json.dump(data, file)


# --- Load contacts from a JSON file ---
def load_contacts():
    global contacts, next_id
    try:
        with open("contacts.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        print("No saved contacts found, starting fresh.")
        contacts = {}
        next_id = 1
        return

    contacts = {}
    for str_id, contact_dict in data.items():
        id = int(str_id)
        contacts[id] = Contact(id, contact_dict["name"], contact_dict["phone"], contact_dict["email"])

    if contacts:
        next_id = max(contacts.keys()) + 1
    else:
        next_id = 1


# --- CLI Menu Loop ---
def main():
    load_contacts()

    while True:
        print("1. Add contact")
        print("2. Search contact")
        print("3. Update contact")
        print("4. Delete contact")
        print("5. Save contacts")
        print("6. Quit")
        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter name: ")
            phone = input("Enter phone (XXX-XXX-XXXX): ")
            email = input("Enter email: ")
            add_contact(name, phone, email)

        elif choice == "2":
            name = input("Enter name to search: ")
            found = search_contact(name)
            if found:
                print(found)

        elif choice == "3":
            id = int(input("Enter id to update: "))
            name = input("Enter new name (leave blank to skip): ")
            phone = input("Enter new phone (leave blank to skip): ")
            email = input("Enter new email (leave blank to skip): ")
            if name == "":
                name = None
            if phone == "":
                phone = None
            if email == "":
                email = None
            update_contact(id, name, phone, email)

        elif choice == "4":
            id = int(input("Enter id to delete: "))
            delete_contact(id)

        elif choice == "5":
            save_contacts()

        elif choice == "6":
            save_contacts()
            print("Goodbye!")
            break

        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()
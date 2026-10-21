contacts = []
try:
    with open("contact.txt", "r") as file:
        lines = file.readlines()
except:
    lines = []

for line in lines:
    cleaned = line.strip()
    parts = cleaned.split(",")
    name = parts[0].strip()
    phone = parts[1].strip()
    email = parts[2].strip()
    contact = {"name": name, "phone": phone, "email": email}
    contacts.append(contact)

while True:
    print("1. add new contact")
    print("2. view contact")
    print("3.quit")
    print("4. delete contact")

    choice = input("Enter choice: ")

    if choice == "1":
        name = input("Name: ")
        phone = input("Phone: ")
        email = input("Email: ")
        contact = {"name": name, "phone": phone, "email": email}
        contacts.append(contact)
        with open("contact.txt", "a") as file:
            file.write(f"{name}, {phone}, {email}\n")

    elif choice == "2":
        for contact in contacts:
            print(contact["name"], contact["phone"], contact["email"])
    elif choice == "3":
        break
    elif choice == "4":
        name_to_delete = input("which name to delete: ")
        for contact in contacts:
            if contact["name"] == name_to_delete:
                contacts.remove(contact)
                break
        else:
            print("contact not found")
    else:
        print("invalid choice")

import psycopg2
from config import load_config

def show_contacts():
    config = load_config("/Users/adilbekpirnazarov/Desktop/pp2/10/PhoneBook/database.ini")
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, first_name, last_name, phone FROM phonebook ORDER BY id;")
                rows = cur.fetchall()
                print("\nCurrent Contacts:")
                print("ID | First Name | Last Name | Phone")
                print("-----------------------------------")
                for row in rows:
                    print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")
                return [row[0] for row in rows]
    except Exception as e:
        print(e)
        return []

def update_contact(contact_id, new_first_name, new_last_name, new_phone):
    sql = """UPDATE phonebook
             SET first_name = %s,
                 last_name = %s,
                 phone = %s
             WHERE id = %s"""
    config = load_config("/Users/adilbekpirnazarov/Desktop/pp2/10/PhoneBook/database.ini")
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (new_first_name, new_last_name, new_phone, contact_id))
                if cur.rowcount == 0:
                    print(f"No contact found with ID {contact_id}.")
                else:
                    print("Contact updated successfully!")
            conn.commit()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    existing_ids = show_contacts()
    if not existing_ids:
        print("No contacts to update.")
    else:
        answer = input("\nDo you want to update a contact? (yes/no): ").strip().lower()
        if answer == "yes":
            try:
                contact_id = int(input("Enter the ID of the contact to update: "))
                if contact_id not in existing_ids:
                    print(f"ID {contact_id} does not exist. No update performed.")
                else:
                    new_first_name = input("Enter new first name: ")
                    new_last_name = input("Enter new last name: ")
                    new_phone = input("Enter new phone: ")
                    update_contact(contact_id, new_first_name, new_last_name, new_phone)
                    show_contacts()
            except ValueError:
                print("Invalid input. ID must be a number.")
        else:
            print("No updates made.")

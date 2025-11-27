import psycopg2
from config import load_config

def list_users():
    config = load_config("/Users/adilbekpirnazarov/Desktop/pp2/10/PhoneBook/database.ini")
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, first_name, last_name, phone FROM phonebook ORDER BY id")
                rows = cur.fetchall()
                if rows:
                    print("\nCurrent contacts:")
                    for row in rows:
                        print(row)
                else:
                    print("\nNo contacts found.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def delete_by_name(first_name):
    sql = "DELETE FROM phonebook WHERE first_name = %s"
    rows_deleted = 0
    config = load_config("/Users/adilbekpirnazarov/Desktop/pp2/10/PhoneBook/database.ini")

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (first_name,))
                rows_deleted = cur.rowcount
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return rows_deleted

if __name__ == '__main__':
    list_users()

    choice = input("\nDo you want to delete a contact? (yes/no): ").strip().lower()
    if choice == "yes":
        name_to_delete = input("Enter the first name to delete: ").strip()
        deleted = delete_by_name(name_to_delete)
        if deleted > 0:
            print(f"\n{deleted} contact(s) with the name '{name_to_delete}' were deleted.")
        else:
            print(f"\nNo contacts found with the name '{name_to_delete}'.")
    else:
        print("\nNo changes made.")

    list_users()
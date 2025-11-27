import psycopg2
from config import load_config
import csv

def insert_user(first_name, last_name, phone):
    sql = "INSERT INTO phonebook(first_name, last_name, phone) VALUES(%s,%s,%s) RETURNING id"
    config = load_config("/Users/adilbekpirnazarov/Desktop/pp2/10/PhoneBook/database.ini")
    user_id = None
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (first_name, last_name, phone))
                user_id = cur.fetchone()[0]
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return user_id

def insert_from_csv(file_path):
    with open("/Users/adilbekpirnazarov/Desktop/pp2/10/PhoneBook/ins_file.txt", newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            insert_user(row[0], row[1], row[2])

if __name__ == '__main__':
    first_name = input("First name: ")
    last_name = input("Last name: ")
    phone = input("Phone: ")
    user_id = insert_user(first_name, last_name, phone)
    print(f"Inserted user id: {user_id}")

    # insert_from_csv('phonebook.csv')
    # SELECT * FROM phonebook;
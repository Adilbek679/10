import psycopg2
from config import load_config

def run_custom_query():
    config = load_config("/Users/adilbekpirnazarov/Desktop/pp2/10/PhoneBook/database.ini")
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                while True:
                    print("\nВведите ваш SQL-запрос (или 'exit' для выхода):")
                    sql = input("SQL> ").strip()
                    if sql.lower() == 'exit':
                        print("Выход...")
                        break
                    if not sql:
                        continue
                    try:
                        cur.execute(sql)
                        if cur.description:
                            rows = cur.fetchall()
                            if rows:
                                for row in rows:
                                    print(row)
                            else:
                                print("Нет данных.")
                        else:
                            conn.commit()
                            print(f"Запрос выполнен, затронуто строк: {cur.rowcount}")
                    except Exception as e:
                        print("Ошибка выполнения SQL:", e)
    except Exception as error:
        print("Ошибка подключения к базе данных:", error)

if __name__ == '__main__':
    run_custom_query()


#SELECT first_name FROM phonebook WHERE id < 10;
#DELETE FROM phonebook WHERE id = 11;
#SELECT * FROM phonebook ORDER BY id DESC;
import psycopg2
from config import load_config

def add_part(part_name, vendor_name):
    """ Add a new part """
    params =  load_config('/Users/adilbekpirnazarov/Desktop/pp2/10/suppliers/database.ini')
    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                cur.execute('CALL add_new_part(%s,%s)', (part_name, vendor_name))
            conn.commit()  # Commit the transaction
    except (Exception, psycopg2.DatabaseError) as error:
        print("Ошибка при вызове процедуры:", error)

if __name__ == '__main__':
    add_part('OLED', 'LG')

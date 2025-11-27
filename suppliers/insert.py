import psycopg2
from config import load_config

def insert_vendor(vendor_name):
    """Insert a single vendor into the vendors table"""
    sql = """INSERT INTO vendors(vendor_name)
             VALUES(%s) RETURNING vendor_id;"""
    vendor_id = None
    config = load_config('/Users/adilbekpirnazarov/Desktop/pp2/10/suppliers/database.ini')
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (vendor_name,))
                row = cur.fetchone()
                if row:
                    vendor_id = row[0]
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return vendor_id

def insert_many_vendors(vendor_list):
    """Insert multiple vendors into the vendors table"""
    sql = "INSERT INTO vendors(vendor_name) VALUES(%s) RETURNING vendor_id;"
    config = load_config('/Users/adilbekpirnazarov/Desktop/pp2/10/suppliers/database.ini')
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.executemany(sql, vendor_list)
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

if __name__ == '__main__':
    # Вставка одного поставщика
    vid = insert_vendor("3M Co.")
    print(f"Inserted vendor_id: {vid}")

    # Вставка нескольких поставщиков
    vendor_data = [
        ('AKM Semiconductor Inc.',),
        ('Asahi Glass Co Ltd.',),
        ('Daikin Industries Ltd.',),
        ('Dynacast International Inc.',),
        ('Foster Electric Co. Ltd.',),
        ('Murata Manufacturing Co. Ltd.',)
    ]
    insert_many_vendors(vendor_data)
    print("Inserted multiple vendors successfully")

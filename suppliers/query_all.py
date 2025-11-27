import psycopg2
from config import load_config

def get_vendors():
    """ Retrieve data using fetchall() """
    config = load_config('/Users/adilbekpirnazarov/Desktop/pp2/10/suppliers/database.ini')
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT vendor_id, vendor_name FROM vendors ORDER BY vendor_name")
                rows = cur.fetchall()

                print("Total rows:", cur.rowcount)
                for row in rows:
                    print(row)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

if __name__ == '__main__':
    get_vendors()

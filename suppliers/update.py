import psycopg2
from config import load_config


def update_vendor(vendor_id, new_name):
    """Update vendor name based on vendor_id"""
    sql = """
        UPDATE vendors
        SET vendor_name = %s
        WHERE vendor_id = %s
    """
    updated_rows = 0

    try:
        params = load_config('/Users/adilbekpirnazarov/Desktop/pp2/10/suppliers/database.ini')
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (new_name, vendor_id))
                updated_rows = cur.rowcount
            conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error:", error)

    finally:
        return updated_rows


if __name__ == '__main__':
    rows = update_vendor(1, "Samsung Electronics")
    print(f"Updated rows: {rows}")

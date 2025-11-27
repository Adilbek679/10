import psycopg2
from config import load_config

def add_part(part_name, vendor_list):
    """ Add a new part and link it to vendor(s) as a transaction """
    
    insert_part = """
        INSERT INTO parts(part_name)
        VALUES(%s) RETURNING part_id;
    """
    
    assign_vendor = """
        INSERT INTO vendor_parts(vendor_id, part_id)
        VALUES(%s, %s);
    """
    
    conn = None
    config = load_config('/Users/adilbekpirnazarov/Desktop/pp2/10/suppliers/database.ini')

    try:
        # Open transaction
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # 1️ Insert new part
                cur.execute(insert_part, (part_name,))
                row = cur.fetchone()
                
                if row:
                    part_id = row[0]
                    print(f"Inserted part '{part_name}' with ID {part_id}")
                else:
                    raise Exception("Failed to retrieve part_id!")
                
                # 2️ Assign vendors
                for vendor_id in vendor_list:
                    cur.execute(assign_vendor, (vendor_id, part_id))
                    print(f" → Assigned vendor {vendor_id} to part {part_id}")
                
                # 3️ Commit transaction
                conn.commit()
                print("Transaction committed successfully!\n")

    except (Exception, psycopg2.DatabaseError) as error:
        if conn:
            conn.rollback()
        print("⚠ Transaction failed — rolled back.")
        print("Error:", error)


if __name__ == '__main__':
    add_part('SIM Tray', (1, 2))
    add_part('Speaker', (3, 4))
    add_part('Vibrator', (5, 6))
    add_part('Antenna', (6, 7))
    add_part('Home Button', (1, 5))
    add_part('LTE Modem', (1, 5))
    
    add_part('Power Amplifier', (99,))

import psycopg2
from config import load_config

def write_blob(part_id, path_to_file, file_extension):
    """ Insert a BLOB into a table """
    params = load_config('/Users/adilbekpirnazarov/Desktop/pp2/10/suppliers/database.ini')

    # Read binary data (rb = read binary)
    data = open("/Users/adilbekpirnazarov/Desktop/pp2/10/suppliers/requirements.txt", 'rb').read()

    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO part_drawings(part_id, file_extension, drawing_data)
                    VALUES (%s, %s, %s)
                """, (part_id, file_extension, psycopg2.Binary(data)))
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Ошибка:", error)

if __name__ == '__main__':
    write_blob(1, 'images/input/simtray.png', 'png')
    write_blob(2, 'images/input/speaker.png', 'png')

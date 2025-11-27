import psycopg2
from config import load_config

def read_blob(part_id, path_to_dir):
    """ Read BLOB data from a table """
    config = load_config('/Users/adilbekpirnazarov/Desktop/pp2/10/suppliers/database.ini')

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT part_name, file_extension, drawing_data
                    FROM part_drawings
                    INNER JOIN parts ON parts.part_id = part_drawings.part_id
                    WHERE parts.part_id = %s
                """, (part_id,))
                blob = cur.fetchone()

                file_path = path_to_dir + blob[0] + '.' + blob[1]
                open("/Users/adilbekpirnazarov/Desktop/pp2/10/suppliers/requirements.txt", 'wb').write(blob[2])
                print(f"Файл сохранен: {file_path}")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Ошибка:", error)

if __name__ == '__main__':
    read_blob(1, 'images/output/')
    read_blob(2, 'images/output/')

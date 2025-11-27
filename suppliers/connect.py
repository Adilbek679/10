import psycopg2
from config import load_config

def connect(config):
    try:
        with psycopg2.connect(**config) as conn:
            print('Connected to the PostgreSQL server.')
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print('Error:', error)

if __name__ == '__main__':
    cfg = load_config('/Users/adilbekpirnazarov/Desktop/pp2/10/suppliers/database.ini')
    connect(cfg)

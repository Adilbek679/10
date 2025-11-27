import psycopg2
from config import load_config

def create_tables():
    config = load_config("/Users/adilbekpirnazarov/Desktop/pp2/10/9/database.ini")  
    commands = [
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS user_score (
            score_id SERIAL PRIMARY KEY,
            user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
            score INT DEFAULT 0,
            level INT DEFAULT 1,
            UNIQUE(user_id)
        )
        """
    ]

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                for command in commands:
                    cur.execute(command)
            conn.commit()
            print("Tables created successfully or already exist.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error creating tables: {error}")

if __name__ == "__main__":
    create_tables()

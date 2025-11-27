import psycopg2
from config import load_config

def get_connection():
    config = load_config("/Users/adilbekpirnazarov/Desktop/pp2/10/9/database.ini")
    return psycopg2.connect(**config)

def get_user(username):
    """Возвращает пользователя по username (id, username, рекорд)"""
    config = load_config("database.ini")
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, username, score FROM users WHERE username=%s", (username,))
                return cur.fetchone()  # (id, username, score) или None
    except Exception as e:
        print(e)
        return None

def create_user(username):
    """Создаёт пользователя с рекордом 0"""
    config = load_config("database.ini")
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO users(username, score) VALUES (%s, 0) RETURNING id", (username,))
                user_id = cur.fetchone()[0]
            conn.commit()
        return user_id
    except Exception as e:
        print(e)
        return None
def get_score(user_id):
    config = load_config("database.ini")
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT score, level FROM user_score WHERE user_id=%s", (user_id,))
                row = cur.fetchone()
                return row if row else (0, 1)
    except Exception as e:
        print(e)
        return (0, 1)

def update_user_score(user_id, score, level):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT score, level FROM user_score WHERE user_id=%s", (user_id,))
    existing = cursor.fetchone()

    if existing:
        old_score, old_level = existing
        score = max(score, old_score)
        level = max(level, old_level)
        cursor.execute(
            "UPDATE user_score SET score=%s, level=%s WHERE user_id=%s",
            (score, level, user_id)
        )
    else:
        cursor.execute(
            "INSERT INTO user_score (user_id, score, level) VALUES (%s, %s, %s)",
            (user_id, score, level)
        )
    connection.commit()
    cursor.close()
    connection.close()



def get_leaderboard():
    config = load_config("database.ini")
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT u.username, s.score, s.level
                    FROM user_score s
                    JOIN users u ON u.id = s.user_id
                    ORDER BY s.score DESC LIMIT 10
                """)
                return cur.fetchall()  # вернёт [(username, score, level), ...]
    except Exception as e:
        print(e)
        return []


import psycopg2
import json
from config import load_config

def save_game(user_id, snake, score, level, direction):
    conn = get_connection()
    cur = conn.cursor()
    snake_json = json.dumps(snake)
    cur.execute("""
        INSERT INTO saved_games(user_id, snake_state, score, level, direction)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (user_id) 
        DO UPDATE SET snake_state=%s, score=%s, level=%s, direction=%s
    """, (user_id, snake_json, score, level, direction, snake_json, score, level, direction))
    conn.commit()
    cur.close()
    conn.close()

def load_game(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT snake_state, score, level, direction FROM saved_games WHERE user_id=%s", (user_id,))
    data = cur.fetchone()
    cur.close()
    conn.close()
    if data:
        snake = data[0]
        score = data[1]
        level = data[2]
        direction = data[3]
        return snake, score, level, direction
    return None
import sqlite3
import json
import os

DB_PATH = 'weights.db'
CACHE_PATH = 'cache.json'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weights (
            name TEXT PRIMARY KEY,
            weight REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def insert_weight(name, weight):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO weights (name, weight) VALUES (?, ?)', (name, weight))
        conn.commit()
    except sqlite3.IntegrityError:
        raise ValueError(f"Запись с именем '{name}' уже существует!")
    finally:
        conn.close()

def get_all_weights():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT name, weight FROM weights')
    rows = cursor.fetchall()
    conn.close()
    return dict(rows)

def load_cache(path=CACHE_PATH):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Файл {path} не найден!")
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

if __name__ == '__main__':
    init_db()

    try:
        cache = load_cache()
        for name, weight in cache.items():
            try:
                insert_weight(name, weight)
            except ValueError as e:
                print(e)
    except Exception as e:
        print(f'Ошибка загрузки или вставки данных: {e}')

    print(get_all_weights())

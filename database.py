import sqlite3
from datetime import datetime

def init_db():
    """Инициализация базы данных"""
    conn = sqlite3.connect('hr_bot.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        username TEXT,
        review_text TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()

def save_review(user_id: int, username: str, review_text: str):
    """Сохраняет отзыв в базу данных"""
    conn = sqlite3.connect('hr_bot.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO reviews (user_id, username, review_text) VALUES (?, ?, ?)",
            (user_id, username, review_text)
        )
        conn.commit()
        print(f"Отзыв сохранен: user_id={user_id}, username={username}")
    except Exception as e:
        print(f"Ошибка при сохранении отзыва: {e}")
    finally:
        conn.close()

# Инициализируем БД при импорте
init_db()
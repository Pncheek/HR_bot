import sqlite3
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, Date, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    username = Column(String)
    review_text = Column(Text)
    review_date = Column(String)

class Notification(Base):
    __tablename__ = 'notifications'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    username = Column(String)
    notification_date = Column(String)
    notification_text = Column(Text)
    chat_id = Column(Integer)

class Database:
    def __init__(self, db_name='bot_database.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def get_all_feedbacks(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT username, review_text as text, date 
        FROM reviews 
        ORDER BY date DESC
        ''')
        return [dict(row) for row in cursor.fetchall()]

    def get_all_survey_responses(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT username, survey_type, response_text as response, date 
        FROM survey_responses 
        ORDER BY date DESC
        ''')
        return [dict(row) for row in cursor.fetchall()]

    def create_tables(self):
        cursor = self.conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            review_text TEXT,
            review_date TEXT
        )
        ''')
        self.conn.commit()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            notification_date TEXT,
            notification_text TEXT,
            chat_id INTEGER
        )
        ''')
        self.conn.commit()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS survey_answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            answer_text TEXT,
            survey_type TEXT,
            answer_date TEXT
        )
        ''')
        self.conn.commit()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_timers (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_message_date TEXT
        )
        ''')

        self.conn.commit()

    def add_review(self, user_id, username, review_text):
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO reviews (user_id, username, review_text, review_date) VALUES (?, ?, ?, ?)''', 
                       (user_id, username, 
                        review_text, 
                        datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        self.conn.commit()

    def add_notification(self, user_id, username, notification_date, notification_text, chat_id):
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO notifications (user_id, username, notification_date, notification_text, chat_id) VALUES (?, ?, ?, ?, ?)''', 
                       (user_id, username, notification_date, notification_text, chat_id))
        self.conn.commit()

    def add_survey_answer(self, user_id, username, answer_text, survey_type):
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO survey_answers (user_id, username, answer_text, survey_type, answer_date) VALUES (?, ?, ?, ?, ?)''', 
                       (user_id, username, answer_text, survey_type, 
                        datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        self.conn.commit()

    def get_user_first_message_date(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT first_message_date FROM user_timers WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        return datetime.strptime(result[0], '%Y-%m-%d %H:%M:%S') if result else None

    def set_user_first_message_date(self, user_id, username):
        cursor = self.conn.cursor()
        cursor.execute('''INSERT OR IGNORE INTO user_timers (user_id, username, first_message_date) VALUES (?, ?, ?) ''', 
                       (user_id, username, 
                        datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        self.conn.commit()

    def close(self):
        self.conn.close()
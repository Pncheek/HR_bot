import sqlite3
from datetime import datetime, timedelta

class Database:
    def __init__(self, db_name='bot_database.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

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

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_timers (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_message_date TEXT
        )
        ''')

        self.conn.commit()

    def add_review(self, user_id, username, review_text):
        cursor = self.conn.curser()
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
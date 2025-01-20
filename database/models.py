import logging
import sqlite3
from math import remainder
from mimetypes import read_mime_types
from typing import List, Tuple


class Database:
    def __init__(self, db_file: str = 'reminders.db'):
        self.db_file = db_file

    def create_tables(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reminders
            (user_id INTEGER,
            name TEXT,
            birth_date TEXT,
            message TEXT,
            early_reminder INTEGER,
            days_before INTEGER)
            """
        )
        conn.commit()
        conn.close()

    def add_reminder(self, user_id:int, name:str, birth_date:str,
                     message:str, early_reminder:bool=False, days_before:int=0):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO reminders (user_id, name, birth_date, message, early_reminder, days_before)
                VALUES(?, ?, ?, ?, ?, ?)""",
            (user_id, name, birth_date, message, early_reminder, days_before)
        )
        conn.commit()
        conn.close()

    def get_user_reminders(self, user_id: int) -> List[Tuple]:
        """
        Get all reminders for a specific user.
        Returns a list of tuples (name, birth_date, message)
        """
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("""
            SELECT name, birth_date, message 
            FROM reminders 
            WHERE user_id = ?
            ORDER BY substr(birth_date, 4, 2), substr(birth_date, 1, 2)
        """, (user_id,))
        reminders = c.fetchall()
        conn.close()
        return reminders

    def get_today_reminders(self, today_date:str) -> List[Tuple]:
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT user_id, name, message FROM reminders WHERE substr(birth_date, 1, 5) = ?",
            (today_date, )
        )
        reminders = cursor.fetchall()
        conn.close()
        return reminders

    def delete_reminder(self, user_id:int, name:str, date:str) -> bool:
        try:
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()
            c.execute("""
                        DELETE FROM reminders 
                        WHERE user_id = ? AND name = ? AND birth_date = ?
                    """, (user_id, name, date))
            conn.commit()
            success = c.rowcount > 0
            conn.close()
            return success
        except Exception as e:
            logging.error(f"Error deleting reminder: {e}")
            return False



























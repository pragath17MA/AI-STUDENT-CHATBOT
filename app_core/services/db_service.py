import sqlite3
import os

class DatabaseService:
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_db()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        """Initializes the database schema if it doesn't already exist."""
        with self.get_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS chats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            # Add an index to speed up history lookups
            conn.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON chats(timestamp)')
            conn.commit()

    def save_message(self, role, content):
        """Persists a chat message to the database."""
        try:
            with self.get_connection() as conn:
                conn.execute(
                    'INSERT INTO chats (role, content) VALUES (?, ?)',
                    (role, content)
                )
                conn.commit()
        except Exception as e:
            print(f"Database error while saving: {e}")

    def get_history(self, limit=20):
        """Retrieves limited chat history, ordered chronologically."""
        try:
            with self.get_connection() as conn:
                rows = conn.execute(
                    'SELECT role, content FROM chats ORDER BY id DESC LIMIT ?',
                    (limit,)
                ).fetchall()
                # Return in chronological order
                return [{"role": row["role"], "content": row["content"]} for row in reversed(rows)]
        except Exception as e:
            print(f"Database error while fetching: {e}")
            return []

    def clear(self):
        """Wipes the entire chat history."""
        with self.get_connection() as conn:
            conn.execute('DELETE FROM chats')
            conn.commit()

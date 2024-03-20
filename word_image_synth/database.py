import os
import sqlite3


class DatabaseManager:
    """
    Class to manage the SQLite database.
    """
    def __init__(self, output_dir):
        """Initialize the database connection."""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        db_file = os.path.join(output_dir, "database.db")
        self.db_file = db_file
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        """Creates the words table if it doesn't already exist."""
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS words
               (word TEXT NOT NULL UNIQUE, lang TEXT NOT NULL)"""
        )
        self.conn.commit()

    async def get_word_count(self, lang):
        """Get the current word count for a specific language."""
        self.cursor.execute("SELECT COUNT(*) FROM words WHERE lang = ?", (lang,))
        count = self.cursor.fetchone()[0]
        return count

    async def save_words_to_db(self, words, lang):
        """Save words to the SQLite database, ignoring duplicates."""
        self.cursor.executemany(
            "INSERT OR IGNORE INTO words (word, lang) VALUES (?, ?)",
            [(word, lang) for word in words],
        )
        self.conn.commit()

    def close(self):
        """Close the database connection."""
        self.conn.close()

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
        self.cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS labels (
            image_name TEXT PRIMARY KEY,
            word TEXT NOT NULL
        )
        """
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

    async def get_words(self, lang, limit=20):

        # check if the database already contains enough words
        current_count = await self.get_word_count(lang)

        # raise an exception if the database does not contain enough words
        if current_count < limit:
            raise ValueError(
                f"The database contains {current_count} words for the language '{lang}', "
                f"which is less than the specified limit of {limit}."
            )

        """Get words from the database."""
        self.cursor.execute(
            "SELECT word FROM words WHERE lang = ? ORDER BY RANDOM() LIMIT ?",
            (lang, limit),
        )
        words = [row[0] for row in self.cursor.fetchall()]
        return words
    
    def save_labels_to_db(self, labels_dict):
        """
        Save labels to the SQLite database.
        """
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        for image_name, word in labels_dict.items():
            c.execute(
                """
                INSERT INTO labels (image_name, word) VALUES (?, ?)
                ON CONFLICT(image_name) DO UPDATE SET word=excluded.word;
            """,
                (image_name, word),
            )
        conn.commit()
        conn.close()
    
    def get_labels(self, lang=None):
        """
        Get labels from the SQLite database.
        """
        if lang:
            self.cursor.execute(
                "SELECT image_name, word FROM labels WHERE lang = ?", (lang,)
            )
        else:
            self.cursor.execute("SELECT image_name, word FROM labels")
        labels = self.cursor.fetchall()

        # convert to a dictionary
        labels = {image_name: word for image_name, word in labels}
        return labels

    def close(self):
        """Close the database connection."""
        self.conn.close()

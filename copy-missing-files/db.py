import sqlite3
import os
class FileIndexDB:
    def __init__(self, db_path):
        self.db_path = db_path
        db_exists = os.path.exists(db_path)
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        if not db_exists:
            self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE files (
                absolute_path TEXT PRIMARY KEY,
                relative_path TEXT,
                size INTEGER,
                created REAL,
                modified REAL,
                checksum TEXT,
                indexed_at REAL
            )
        ''')
        self.conn.commit()

    def add_file(self, file_info):
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO files
                (absolute_path, relative_path, size, created, modified, checksum, indexed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                file_info['absolute_path'],
                file_info['relative_path'],
                file_info['size'],
                file_info['created'],
                file_info['modified'],
                file_info['checksum'],
                file_info['indexed_at']
            ))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Database error during add_file: {e}")

    def add_files(self, file_infos):
        try:
            data = [(
                fi['absolute_path'],
                fi['relative_path'],
                fi['size'],
                fi['created'],
                fi['modified'],
                fi['checksum'],
                fi['indexed_at']
            ) for fi in file_infos]
            self.cursor.executemany('''
                INSERT OR REPLACE INTO files
                (absolute_path, relative_path, size, created, modified, checksum, indexed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', data)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Database error during add_files: {e}")

    def remove_file(self, absolute_path):
        try:
            self.cursor.execute('''
                DELETE FROM files WHERE absolute_path = ?
            ''', (absolute_path,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Database error during remove_file: {e}")

    def close(self):
        self.conn.close()

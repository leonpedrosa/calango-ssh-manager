import os
import sqlite3

# Verify BD
def check_sqlite_exist():
    if not os.path.exists('sqlite.'):
        conn = sqlite3.connect('views/sqlite.db')
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='conexoes'")
        table_exists = cursor.fetchone()
        if not table_exists:
            cursor.execute('''
            CREATE TABLE conexoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT,
                    host TEXT,
                    port INT,
                    usuario TEXT,
                    senha TEXT)'''
            )
            conn.commit()
            conn.close()
        return 1
    else:
        return 0

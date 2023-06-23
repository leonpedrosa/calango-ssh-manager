import os
import sqlite3

# Verify BD
def check_sqlite():
    if not os.path.exists('sqlite.'):
        conn = sqlite3.connect('sqlite.db')
        conn.close()
        return 1
    else:
        return 0

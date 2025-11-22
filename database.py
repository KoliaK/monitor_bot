import sqlite3
from datetime import datetime

# We remove the global 'conn' variable. 
# Each function should manage its own connection to be safe.

def create_table():
    # "with" automatically closes the connection when done
    with sqlite3.connect('books.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                price REAL, 
                timestamp TEXT
            );
        ''')
        conn.commit()

def store_book(title, price):
    # Ensure table exists before inserting (or call this once in main.py)
    create_table()
    
    current_date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with sqlite3.connect('books.db') as conn:
        cursor = conn.cursor()
        
        # 1. FIX: Removed {} around variables
        # 2. FIX: Using standard SQL string (no f-string needed for the query part)
        cursor.execute(
            'INSERT INTO prices (title, price, timestamp) VALUES (?, ?, ?)', 
            (title, price, current_date_time)
        )
        conn.commit()
        
        # strict checking: print strictly what was added
        print(f"Saved: {title} | ${price}")
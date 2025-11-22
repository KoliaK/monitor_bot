import sqlite3
from datetime import datetime

# Creates connector and cursor
conn = sqlite3.connect('books.db')
cursor = conn.cursor()

def create_table():
    try:
        # Creates Table
        table_prices = '''
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            price FLOAT,
            timestamp DATETIME
        );
    ''' 
        cursor.execute(table_prices)
        
        conn.commit()
    
    except sqlite3.Error as e:
        print(f'SQLite error: {e}')
    

def store_book(title, price):
    create_table()
    current_date_time = datetime.now()
    cursor.execute(f'INSERT INTO prices (title, price, timestamp) VALUES (?, ?, ?)', (title, price, current_date_time))
    conn.commit()
    print('Inserted Data:')
    cursor.execute('SELECT * FROM prices')
    for row in cursor:
        print(row)
    conn.close()
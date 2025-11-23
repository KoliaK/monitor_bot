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

        cursor.execute(
            'INSERT INTO prices (title, price, timestamp) VALUES (?, ?, ?)', 
            (title, price, current_date_time)
        )
        conn.commit()
        
        # strict checking: print strictly what was added
        print(f"Saved: {title} | ${price}")


def get_analytics():

    create_table()
    
    with sqlite3.connect('books.db') as conn:
        cursor = conn.cursor()
        # Get Total Count of Books
        cursor.execute('SELECT COUNT(*) FROM prices')
        # fetchone() returns a tuple, so we want the first item
        total_books = cursor.fetchone()[0]
        
        # Get AVG Price
        cursor.execute('SELECT COUNT(*), AVG(price) FROM prices')
        average_price = cursor.fetchone()[0]

        # Get Cheapest Book
        cursor.execute(
            '''
                SELECT title, price FROM prices
                ORDER BY price ASC
                LIMIT 1
            '''
        )
        # This time we want the entire tuple ('The Book Title', 12.99)
        cheapest_book_data = cursor.fetchone()

        # Handling the case where DB might be empty
        if cheapest_book_data:
            cheapest_title = cheapest_book_data[0]
            cheapest_price = cheapest_book_data[1]
        else:
            cheapest_title = 'N/A'
            cheapest_price = 0.0

        print(
            f"""
                --- REPORT ---
                Total Books Tracked: {total_books}
                Average Price: £{average_price}
                Cheapest Book: "{cheapest_title}" at £{cheapest_price}
            """
        )
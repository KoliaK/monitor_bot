import requests
import json
from bs4 import BeautifulSoup
import sys
import re
import schedule
import time
import os
from dotenv import load_dotenv

# Scripts
import database
import notifications

# this loads environment variables from .env file
load_dotenv()
# url is fetched from .env file 
url = os.getenv('TARGET_URL')

ALERT_THRESHOLD = 50.0

def request_getter(url: str) -> str:
    try:
        response = requests.get(url, timeout=10) 
        response.raise_for_status()
        response.encoding = 'utf-8'
        print(f"Connection Successful: Status Code {response.status_code}")
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Network Error: {e}")
        sys.exit(1)

# this removes the £ symbol from price. 
# the easiest way would be just use float(price[1::]) 
# but wouldn't work on R$, for example
def clean_price(price: str) -> float:
    stripped_price = re.sub(r'[^0-9.]', '', price)
    return float(stripped_price)
    
def job() -> None:
    html_content = request_getter(url)
    # Scraps HTML Tags
    soup = BeautifulSoup(html_content, 'html.parser')
    # Retrieves 5 Five Books That are Stored in Article tags 
    book_cards = soup.find_all('article', class_='product_pod', limit=5)
    # List to be Filled With Dictionaries for JSON
    books_data = []

    print(f"\n--- Found {len(book_cards)} books ---\n")

    for card in book_cards:
        # Looks for the Titles Inside the Articles
        title_tag = card.find('h3').find('a')
        # Makes Sure the Entire Title is Retrieved to avoid shorteners like (...)
        title = title_tag['title'] 
        # Looks For The Price Inside Each book_card
        price_tag = card.find('p', class_='price_color')
        # Cleans any Currency Symbols And Converts The Price to Float
        price = clean_price(price_tag.text)
        # Adds a Dict to the List to be Stored in a Json
        books_data.append({'Book Title': title, 'Book Price': price})
        # Adds to the database
        database.store_book(title, price)

        # use if necessary to debug
        print(f"Book: {title}")
        print(f"Price: {price}")
        # Price Alert
        if price < ALERT_THRESHOLD:
            notifications.send_alert(f"🚨Low price found! {title} is £{price}🚨")
        print("-" * 20)
        
    # retrieves all books from books.db
    # prints out the AVG and Cheapest price
    database.get_analytics()

    # JSON WRITE FILE
    try:
        with open('books.json', 'w', encoding='utf-8') as file:
            json.dump(books_data, file, indent=4)
            print('Data successfuly written to books.json')
    # Prints out the Input/Output error in case of failing to write the Json file       
    except IOError as e:
        print(f'Error writing to file: {e}')

if __name__ == '__main__':
    schedule.every(1).minutes.do(job)
    print('Monitor started... Waiting for schedule.')
    
    while True:
        schedule.run_pending()
        time.sleep(1)
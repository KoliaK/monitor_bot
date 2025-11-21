import requests
import json
from bs4 import BeautifulSoup
import sys
import re

url = 'http://books.toscrape.com/'

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
    
def parse_books() -> None:
    html_content = request_getter(url)
    # Scraps HTML Tags
    soup = BeautifulSoup(html_content, 'html.parser')
    # Retrieves 5 Five Books That are Stored in Article tags 
    book_cards = soup.find_all('article', class_='product_pod', limit=5)
    # List to be Filled With Dictionaries Containing Books Name and Price 
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

        # use if necessary to debug
        # print(f"Book: {title}")
        # print(f"Price: {price}")
        # print("-" * 20)

    try:
        with open('books.json', 'w', encoding='utf-8') as file:
            json.dump(books_data, file, indent=4)
            print('Data successfuly written to books.json')
    # I'm not sure what IOError means, and 'e'. What this does?        
    except IOError as e:
        # I'm completely clueless of why to include {e} here.
        print(f'Error writing to file: {e}')

if __name__ == '__main__':
    parse_books()
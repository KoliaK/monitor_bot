import requests
from bs4 import BeautifulSoup

url = 'http://books.toscrape.com/'

def request_getter(url: str) -> str:
    response = requests.get(url, timeout=5)
    html_content = response.text

    try: 
        response.raise_for_status()
        print(f"Connection Succesful: Status Code {response.status_code}")
        return html_content
    except requests.exceptions.ConnectionError as e:
        print(f"Connection Error: Could not connect to the server. Is the internet down? {e}")
    except requests.exceptions.Timeout as e:
        print(f"Timeout Error: The request timed out. {e}")
    except requests.exceptions.RequestException as e:
        print(f"An unexpected request error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        print("Connection attempt finished.")
    

def parse_books():
    html_content = request_getter(url)
    soup = BeautifulSoup(html_content, 'html.parser')
    titles = soup.find_all(article_class='h3', limit=5)
    prices = soup.find_all(article_class='price_color', limit=5)
    books = {
        titles : prices
    }
    for title, price in books:
        print(books[title])
        print(books[price])


if __name__ == '__main__':
    parse_books()
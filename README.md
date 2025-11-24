# 📚 Book Price Monitor

## 🚀 Overview
An automated Python-based ETL pipeline that monitors book prices on e-commerce platforms. The application scrapes product data, cleanses it, stores historical trends in a SQLite database, and triggers real-time alerts when prices drop below a specified threshold.

**Target Site:** [Books to Scrape](http://books.toscrape.com/) (Sandbox environment)

## 🏗️ Architecture
The project follows a modular **ETL (Extract, Transform, Load)** architecture:
1.  **Extract:** `requests` & `BeautifulSoup` scrape raw HTML data.
2.  **Transform:** `re` (Regex) cleans currency strings and data types.
3.  **Load:** Data is upserted into `SQLite` with idempotency checks to prevent duplicates.
4.  **Alert:** Custom logic triggers notifications (Console/Discord) based on price thresholds.

## 🛠️ Tech Stack
* **Python 3.10+**
* **BeautifulSoup4:** HTML Parsing
* **SQLite3:** Relational Database & Persistence
* **Schedule:** Task orchestration (CRON-like behavior)
* **Python-Dotenv:** Environment variable management
* **Git:** Version Control

## ⚙️ Setup & Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/monitor_bot.git](https://github.com/YOUR_USERNAME/monitor_bot.git)
    cd monitor_bot
    ```

2.  **Create a Virtual Environment:**
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # Mac/Linux
    source .venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configuration:**
    Create a `.env` file in the root directory:
    ```env
    TARGET_URL=http://books.toscrape.com/
    ```

## 🏃 Usage
Run the monitor:
```bash
python main.py

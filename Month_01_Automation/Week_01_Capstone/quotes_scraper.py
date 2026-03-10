import requests
from bs4 import BeautifulSoup
import sqlite3
import schedule
import time


class Scraper:
    def __init__(self, url):
        self.url = url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        self.session = requests.session()
        self.setup_db()

    def fetch_page(self):
        print(f"Fetching: {self.url}")
        try:
            response = self.session.get(self.url, headers=self.headers, timeout=25)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch page content: {e}")
            return None

    def extract_data(self):
        html_content = self.fetch_page()
        if not html_content:
            return []
        print("Parsing the html content")
        soup = BeautifulSoup(html_content, "html.parser")

        quotes_data = []
        for quote_block in soup.find_all("div", class_="quote")[:5]:
            text = quote_block.find("span", class_="text").get_text(strip=True)
            author = quote_block.find("small", class_="author").get_text(strip=True)
            quotes_data.append((text, author))
        return quotes_data

    def setup_db(self):
        conn = sqlite3.connect("quotes.db")
        cursor = conn.cursor()

        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS quotes (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       quote TEXT UNIQUE,
                       author TEXT
                )
        """)
        conn.commit()
        conn.close()
        print("Database setup complete. Fortress secured.")

    def save_to_db(self, data):
        if not data:
            return
        conn = sqlite3.connect("quotes.db")
        cursor = conn.cursor()
        try:
            for quote, author in data:
                cursor.execute(
                    """
                    INSERT OR IGNORE INTO quotes (quote, author)
                    VALUES (?, ?)
                    """,
                    (quote, author),
                )
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        conn.commit()
        conn.close()
        print("Save Complete")


def run_automation():
    print("\n--- Firing the Quote Extraction Engine ---")
    scraper = Scraper("http://quotes.toscrape.com")
    info = scraper.extract_data()
    scraper.save_to_db(info)
    print("Waiting for the next scheduled run...\n")


if __name__ == "__main__":
    run_automation()
    schedule.every(10).minutes.do(run_automation)
    print("Bot is alive. Press Ctrl+C to kill the engine.")
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nEngine manually shut down.")

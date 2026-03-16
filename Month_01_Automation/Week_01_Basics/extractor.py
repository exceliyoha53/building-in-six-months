import sqlite3
import schedule
import time
import requests
from bs4 import BeautifulSoup


class LeadExtractor:
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        self.session = requests.Session()  # A session keeps our connection alive and holds cookies
        self.db_name = "leads.db"
        self.setup_database()

    def setup_database(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # SQL to create a table:
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS articles(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       title TEXT NOT NULL,
                       link TEXT UNIQUE NOT NULL
                )
        """)
        conn.commit()
        conn.close()
        print("Database setup complete. Fortress secured.")

    def fetch_page(self):
        print(f"\nFetching: {self.base_url}")
        try:
            response = self.session.get(self.base_url, headers=self.headers, timeout=15)
            response.raise_for_status()  # 404:page not found|403:forbidden|500: server error
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Connection failed: {e}")
            return None

    def extract_data(self):
        html_content = self.fetch_page()
        if not html_content:
            return []

        print("Parsing the data...\n")
        soup = BeautifulSoup(html_content, "html.parser")

        extracted_leads = []

        articles = soup.find_all("tr", class_="athing", limit=5)
        for article in articles:
            title_tag = soup.find("span", class_="titleline").find("a")
            title = title_tag.getText()
            link = title_tag.get("href")

            lead_data = {"Title": title, "Link": link}
            extracted_leads.append(lead_data)
        return extracted_leads

    def save_to_db(self, data):
        if not data:
            return
        print(f"Attempting to save {len(data)} leads to database...")
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        new_inserts = 0
        for item in data:
            try:
                cursor.execute(
                    """
                    INSERT OR IGNORE INTO articles (title, link)
                    VALUES(?, ?)
                """,
                    (item["Title"], item["Link"]),
                )
                if cursor.rowcount == 1:  # if row was added(1) or not(0)
                    new_inserts += 1
            except sqlite3.Error as e:
                print(f"Database error: {e}")

        conn.commit()
        conn.close()
        print(f"Save complete! {new_inserts} new unique leads added to the fortress. \n")


def run_automation():
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{current_time}] Firing the extraction engine...")

    target_site = "https://news.ycombinator.com/"
    my_scraper = LeadExtractor(target_site)

    scraped_data = my_scraper.extract_data()
    my_scraper.save_to_db(scraped_data)
    print("Waiting for the next schedule to run...")


if __name__ == "__main__":
    schedule.every(1).minutes.do(run_automation)
    print("Automation engine started. Press Ctrl+C in the terminal to stop it.\n")
    run_automation()

    while True:
        schedule.run_pending()
        time.sleep(1)

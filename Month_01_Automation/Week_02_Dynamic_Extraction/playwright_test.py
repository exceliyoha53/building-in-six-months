from playwright.sync_api import sync_playwright
import sqlite3


def scrape_multiple_pages():
    print("Deploying Intelligent ghost browser...\n")
    quotes_data = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://quotes.toscrape.com/js/")
        page_number = 1
        total_quotes_scraped = 0
        while True:
            print(f"--- Scraping Page {page_number} ---")
            page.wait_for_selector("div.quote")
            quotes_on_page = page.query_selector_all("div.quote")
            total_quotes_scraped += len(quotes_on_page)

            for quote_element in quotes_on_page:
                quote = quote_element.query_selector("span.text").inner_text()
                author = quote_element.query_selector("small.author").inner_text()
                quotes_data.append((quote, author))

            next_button = page.locator("li.next > a")
            if next_button.count() > 0:
                print("Clicking Next...\n")
                next_button.click()
                page.wait_for_load_state("networkidle")
                page_number += 1
            else:
                print("\nNo 'Next' button found. Reached the end of the catalog.")
                break

        print("-" * 40)
        print(
            f"Mission complete. Scraped a total of {total_quotes_scraped} quotes across {page_number} pages."
        )
        browser.close()
    return quotes_data


def setup_db():
    conn = sqlite3.connect("js_quotes.db")
    cursor = conn.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS new_quotes(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   quote TEXT UNIQUE,
                   author TEXT
            )
    """)
    conn.commit()
    conn.close()
    print("Database setup complete. Fortress secured.")


def save_to_db(data):
    if not data:
        return
    conn = sqlite3.connect("js_quotes.db")
    cursor = conn.cursor()
    try:
        for quote, author in data:
            cursor.execute(
                """
                INSERT OR IGNORE INTO new_quotes (quote, author)
                VALUES (?, ?)
                """,
                (quote, author),
            )
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    conn.commit()
    conn.close()
    print("Save Complete")


if __name__ == "__main__":
    setup_db()
    data = scrape_multiple_pages()
    save_to_db(data)

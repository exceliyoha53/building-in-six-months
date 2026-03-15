from playwright.sync_api import sync_playwright
import sqlite3


def init_db():
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            title TEXT,
            price TEXT,
            availability TEXT,
            link TEXT UNIQUE
        )
    """)
    conn.commit()
    conn.close()


def save_book(title, price, availability, link):
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO books (title, price, availability, link)
            VALUES (?, ?, ?, ?)
        """,
            (title, price, availability, link),
        )
        conn.commit()

    except sqlite3.IntegrityError:
        pass
    finally:
        conn.close()


def scrape_booksite():

    init_db()

    with sync_playwright() as p:
        page_number = 1
        total_books = 0
        print("Iitializing dynamic ghost browser...")
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        print("Navigating to target...\n")
        page.goto("https://books.toscrape.com/", timeout=60000, wait_until="domcontentloaded")

        while True:
            print(f"--- Scraping Page {page_number} ---")
            book_Card = page.locator("article.product_pod")
            book_Card.first.wait_for()
            books_on_page = book_Card.count()
            print(f"Breach Successful! Located {books_on_page} books on the page")

            for i in range(books_on_page):
                card = book_Card.nth(i)
                title_element = card.locator("h3 a")
                title = title_element.get_attribute("title")
                link = title_element.get_attribute("href")

                price = card.locator("div.product_price p.price_color").inner_text().strip()
                availability = (
                    card.locator("div.product_price p.instock.availability").inner_text().strip()
                )
                full_link = (
                    f"https://books.toscrape.com/{link}" if not link.startswith("http") else link
                )

                save_book(title, price, availability, full_link)

            total_books += books_on_page
            print(f"Total so far: {total_books}")

            next_button = page.locator("li.next > a")
            if next_button.count() == 0:
                print("No next button found -> done")
                break

            print("Clicking Next...\n")
            next_button.click()
            page.wait_for_load_state("networkidle")
            page_number += 1

        print("-" * 40)
        print(
            f"Mission complete. Scraped a total of {total_books} quotes across {page_number} pages."
        )
        browser.close()


if __name__ == "__main__":
    scrape_booksite()

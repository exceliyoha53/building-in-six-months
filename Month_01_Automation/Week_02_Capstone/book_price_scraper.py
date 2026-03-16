from playwright.sync_api import sync_playwright
import sqlite3
import logging

logger = logging.getLogger(__name__)


def init_db():
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            title TEXT,
            price TEXT,
            availability TEXT,
            link TEXT UNIQUE,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
    logger.info("Book vault initialized and secured.")


def save_books_to_vault(books_data):
    if not books_data:
        return
    logger.info(f"Attempting to batch save {len(books_data)} books...")
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    new_inserts = 0
    for book in books_data:
        try:
            cursor.execute(
                """
                INSERT INTO books (title, price, availability, link, last_updated)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(link) 
                DO UPDATE SET 
                    price = excluded.price,
                    availability = excluded.availability,
                    last_updated = CURRENT_TIMESTAMP
            """,
                (book["title"], book["price"], book["availability"], book["full_link"]),
            )
            if cursor.rowcount > 0:
                new_inserts += 1
        except sqlite3.Error as e:
            logger.error(f"Database Error during insertion: {e}")

    conn.commit()
    conn.close()
    logger.info(f"Successfully locked {new_inserts} new books into the vault.")


def scrape_and_save_booksite():
    init_db()
    extracted_books = []

    logger.info("Deploying dynamic ghost browser to Bookscape...")
    with sync_playwright() as p:
        page_number = 1
        total_books = 0

        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            page.goto("https://books.toscrape.com/", timeout=100000, wait_until="domcontentloaded")

            while True:
                logger.info(f"--- Scraping Page {page_number} ---")

                page.wait_for_selector("article.product_pod", timeout=100000)
                book_Card = page.locator("article.product_pod")
                books_on_page = book_Card.count()
                logger.info(f"Breach Successful! Located {books_on_page} books on the page")

                for i in range(books_on_page):
                    card = book_Card.nth(i)
                    title_element = card.locator("h3 a")
                    title = title_element.get_attribute("title")
                    link = title_element.get_attribute("href")

                    price = card.locator("div.product_price p.price_color").inner_text().strip()
                    availability = (
                        card.locator("div.product_price p.instock.availability")
                        .inner_text()
                        .strip()
                    )
                    full_link = (
                        f"https://books.toscrape.com/{link}"
                        if not link.startswith("http")
                        else link
                    )

                    extracted_books.append(
                        {
                            "title": title,
                            "price": price,
                            "availability": availability,
                            "full_link": full_link,
                        }
                    )

                total_books += books_on_page

                next_button = page.locator("li.next > a")
                if next_button.count() == 0:
                    logger.info("No next button found -> End of catalog.")
                    break

                next_button.click()
                page.wait_for_load_state("networkidle")
                page_number += 1

            logger.info(f"Extraction sequence complete. Total books pulled: {total_books}")
            save_books_to_vault(extracted_books)

        except Exception as e:
            logger.error(f"Scraper failed during execution: {e}", exc_info=True)

        finally:
            browser.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    scrape_and_save_booksite()

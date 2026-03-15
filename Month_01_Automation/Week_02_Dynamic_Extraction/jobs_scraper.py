from playwright.sync_api import sync_playwright
import sqlite3
import logging


logger = logging.getLogger(__name__)


def setup_job_vault():
    conn = sqlite3.connect("remote_jobs.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            company TEXT,
            location TEXT,
            UNIQUE(title, company, location)
        )
    """)
    conn.commit()
    conn.close()
    logger.info("Database setup complete. Job Vault secured.")


def hunt_for_jobs():
    logger.info("Deploying ghost browser to the job board...")
    extracted_jobs = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        logger.info("Infiltrating target URL...")
        try:
            page.goto(
                "https://realpython.github.io/fake-jobs/",
                timeout=60000,
                wait_until="domcontentloaded",
            )
            logger.info("Scanning for jobs...")
            job_cards = page.locator("div.card-content")
            job_cards.first.wait_for()
            total_cards = job_cards.count()
            logger.info(f"Breach successful! Located {total_cards} jobs postings.")
            for i in range(total_cards):
                single_card = job_cards.nth(i)
                title = single_card.locator("h2.title").inner_text().strip()
                company = single_card.locator("h3.company").inner_text().strip()
                location = single_card.locator("p.location").inner_text().strip()

                extracted_jobs.append((title, company, location))
        except Exception as e:
            logger.error(f"Failed to extract jobs: {e}", exc_info=True)
        finally:
            browser.close()
    return extracted_jobs


def save_to_vault(jobs_data):
    if not jobs_data:
        print("No data extracted. Aborting save.")
        return
    conn = sqlite3.connect("remote_jobs.db")
    cursor = conn.cursor()
    new_records = 0
    for title, company, location in jobs_data:
        try:
            cursor.execute(
                """
                INSERT OR IGNORE INTO jobs (title, company, location)
                VALUES (?, ?, ?)
            """,
                (title, company, location),
            )

            if cursor.rowcount > 0:
                new_records += 1

        except sqlite3.Error as e:
            logger.error(f"Database error during insert: {e}")

    conn.commit()
    conn.close()
    logger.info(f"Mission Complete! Safely locked {new_records} new remote jobs into the vault.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    setup_job_vault()
    live_data = hunt_for_jobs()
    save_to_vault(live_data)

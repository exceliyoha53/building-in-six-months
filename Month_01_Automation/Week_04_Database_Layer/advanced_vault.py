import sqlite3
import logging

logger = logging.getLogger(__name__)


def setup_tracking_vault():
    conn = sqlite3.connect("price_tracker.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS product_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT UNIQUE,
            current_price TEXT,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
    logger.info("Advanced tracking vault initialized.")


def upsert_product_data(product_name, price):
    """
    Inserts a new product. If the product already exists, it updates the price
    and the last_updated timestamp.
    """
    conn = sqlite3.connect("price_tracker.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO product_prices (product_name, current_price, last_updated)
            VALUES (?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(product_name) 
            DO UPDATE SET 
                current_price = excluded.current_price,
                last_updated = CURRENT_TIMESTAMP
        """,
            (product_name, price),
        )

        conn.commit()
        logger.info(f"UPSERT successful for: {product_name} -> {price}")

    except sqlite3.Error as e:
        logger.error(f"Database error during UPSERT: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    setup_tracking_vault()
    logger.info("--- Simulating Day 1 Scrape ---")
    upsert_product_data("Python Automation Guide", "$45.00")

    logger.info("--- Simulating Day 2 Scrape (Price Drop) ---")
    upsert_product_data("Python Automation Guide", "$29.99")

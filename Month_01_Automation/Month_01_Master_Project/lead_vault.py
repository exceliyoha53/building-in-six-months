import logging
import sqlite3

logger = logging.getLogger(__name__)


def init_vault():
    conn = sqlite3.connect("b2b_leads.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            business_name TEXT,
            website TEXT UNIQUE,
            phone TEXT,
            last_verified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
    logger.info("B2B Lead Vault initialized and secured.")


def upsert_lead(business_name, website, phone):
    """
    Inserts a new business lead. If the website already exists in the vault,
    it updates the phone number and refreshes the last_verified timestamp.
    """
    if not website:
        return
    conn = sqlite3.connect("b2b_leads.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO leads (business_name, website, phone, last_verified)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(website) 
            DO UPDATE SET 
                business_name = excluded.business_name,
                phone = excluded.phone,
                last_verified = CURRENT_TIMESTAMP
        """,
            (business_name, website, phone),
        )

        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Database error during UPSERT: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    init_vault()

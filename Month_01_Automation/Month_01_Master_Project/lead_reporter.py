import sqlite3
import csv
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def generate_lead_report():
    """
    Extracts verified leads from the B2B vault and packages them into a CSV deliverable.
    """
    logger.info("Initiating B2B Lead Report Generation...")

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"b2b_leads_report_{timestamp}.csv"

    try:
        conn = sqlite3.connect("b2b_leads.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT business_name, website, phone, last_verified FROM leads ORDER BY last_verified DESC"
        )
        leads_data = cursor.fetchall()

        if not leads_data:
            logger.warning("Vault is currently empty. No report generated.")
            return

        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Business Name", "Website", "Phone Number", "Last Verified"])
            writer.writerows(leads_data)

        logger.info(
            f"Client deliverable successfully generated: {filename} ({len(leads_data)} verified leads)"
        )

    except sqlite3.Error as e:
        logger.error(f"Failed to access vault during reporting: {e}", exc_info=True)
    except IOError as e:
        logger.error(f"Failed to write CSV file: {e}", exc_info=True)
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    generate_lead_report()

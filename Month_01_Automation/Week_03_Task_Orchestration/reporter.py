import sqlite3
import csv
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def generate_jobs_report():
    """
    Extracts data from the remote_jobs.db vault and formats it into a CSV report.
    """
    logger.info("Initiating Jobs Report Generation...")

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"remote_jobs_report_{timestamp}.csv"
    try:
        conn = sqlite3.connect("remote_jobs.db")
        cursor = conn.cursor()

        cursor.execute("SELECT title, company, location FROM jobs")
        jobs_data = cursor.fetchall()
        if not jobs_data:
            logger.warning("Vault is empty, No report generated.")
            return

        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Job Title", "Company", "Location"])
            writer.writerows(jobs_data)
        logger.info(f"Report successfully generated: {filename} ({len(jobs_data)} records)")

    except sqlite3.Error as e:
        logger.error(f"Failed to access database during reporting: {e}", exc_info=True)
    except IOError as e:
        logger.error(f"Failed to write CSV file: {e}", exc_info=True)
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    generate_jobs_report()

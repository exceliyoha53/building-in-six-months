import logging
import sys
from pathlib import Path
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger

current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

from Week_02_Dynamic_Extraction.jobs_scraper import setup_job_vault, hunt_for_jobs, save_to_vault  # noqa: E402
from Week_02_Capstone.book_price_scraper import init_db, scrape_and_save_booksite  # noqa: E402

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("system.log"), logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)


def remote_job_extraction_task():
    """
    Extracts and save data from https://realpython.github.io/fake-jobs/ to a database
    """
    logger.info("== INITIATING REMOTE JOB EXTRACTION SEQUENCE ==")
    try:
        setup_job_vault()
        live_data = hunt_for_jobs()
        save_to_vault(live_data)

        logger.info("== TASK CYCLE COMPLETE. GHOST BROWSER SLEEPING. ==")

    except Exception as e:
        logger.error(f"Critical failure during extraction: {e}", exc_info=True)


def remote_book_extraction_task():
    """
    scrapes data from https://books.toscrape.com/ and saves in a database
    """
    logger.info("== INITIATING REMOTE BOOK EXTRACTION SEQUENCE ==")
    try:
        init_db()
        scrape_and_save_booksite()
        logger.info("== FULL TASK CYCLE COMPLETE. GHOST BROWSER SLEEPING. ==")
    except Exception as e:
        logger.error(f"Critical failure Scraping books: {e}", exc_info=True)


def main():
    logger.info("Booting up the Core Automation Engine...")
    scheduler = BlockingScheduler()

    scheduler.add_job(
        remote_job_extraction_task,
        trigger=IntervalTrigger(minutes=2),
        id="job_scraper_01",
        name="Remote Jobs Scraper",
        replace_existing=True,
    )
    scheduler.add_job(
        remote_book_extraction_task,
        trigger=IntervalTrigger(minutes=5),
        id="book_scraper_02",
        name="Remote Books Scraper",
        replace_existing=True,
    )
    try:
        logger.info("Scheduler active. Entering autonomous mode.")
        logger.info("Waiting for the first trigger (1 minutes)...")
        logger.info("Waiting for the second trigger (1 minutes)...")
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Admin override detected. Shutting down engine gracefully.")


if __name__ == "__main__":
    main()

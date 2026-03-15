import logging
import sys
from pathlib import Path
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger

current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

from Week_02_Dynamic_Extraction.jobs_scraper import setup_job_vault, hunt_for_jobs, save_to_vault

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("system.log"), logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)


def remote_job_extraction_task():
    """
    The actual sequence the Manager tells the Worker to execute.
    """
    logger.info("== INITIATING REMOTE JOB EXTRACTION SEQUENCE ==")
    try:
        setup_job_vault()
        live_data = hunt_for_jobs()
        save_to_vault(live_data)

        logger.info("== TASK CYCLE COMPLETE. GHOST BROWSER SLEEPING. ==")

    except Exception as e:
        logger.error(f"Critical failure during extraction: {e}", exc_info=True)


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

    try:
        logger.info("Scheduler active. Entering autonomous mode.")
        logger.info("Waiting for the first trigger (2 minutes)...")
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Admin override detected. Shutting down engine gracefully.")


if __name__ == "__main__":
    main()

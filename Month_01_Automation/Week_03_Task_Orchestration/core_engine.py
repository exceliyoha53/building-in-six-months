import logging
import sys
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger


# Never use print() for production scripts. This config outputs to
# BOTH the terminal and a permanent 'system.log' file.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("system.log"), logging.StreamHandler(sys.stdout)],
)

# Initialize the logger for this specific file
logger = logging.getLogger(__name__)


def remote_job_extraction_task():
    """
    Simulated extraction job.
    In production, you will call your Playwright scraper here.
    """
    logger.info("Initiating ghost browser deployment...")
    try:
        # Example of where your Playwright logic would go:
        # extracted_jobs = hunt_for_jobs()
        # save_to_vault(extracted_jobs)

        logger.info("Extraction successful. Vault secured.")

    except Exception as e:
        logger.error(f"Critical failure during extraction: {e}", exc_info=True)


def main():
    logger.info("Booting up the Automation Engine...")
    scheduler = BlockingScheduler()

    scheduler.add_job(
        remote_job_extraction_task,
        trigger=IntervalTrigger(minutes=15),
        id="job_scraper_01",
        name="Remote Jobs Scraper",
        replace_existing=True,
    )

    try:
        logger.info("Scheduler active. Entering autonomous mode.")
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Admin override detected. Shutting down engine gracefully.")


if __name__ == "__main__":
    main()

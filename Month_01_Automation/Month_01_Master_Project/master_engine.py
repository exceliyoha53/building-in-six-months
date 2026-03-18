import sys
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger

from lead_vault import init_vault
from lead_scraper import B2BLeadExtractor
from lead_reporter import generate_lead_report

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("master_system.log"), logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)


def scraping_sequence():
    """Worker 1: The Extraaction Task"""
    logger.info("== INITIATING TARGETED EXTRACTION SEQUENCE ==")
    try:
        # -------------------------------------------------------------------
        # TARGET ACQUISITION CONFIGURATION
        # Note for deployment: Replace the sandbox URL with the client's
        # actual target directory. Ensure CSS selectors in B2BLeadExtractor
        # are updated to match the target's DOM structure.
        # -------------------------------------------------------------------
        sandbox_target = "https://scrapethissite.com/pages/"
        engine = B2BLeadExtractor(target_url=sandbox_target)
        engine.extract_directory()
        logger.info("== EXTRACTION SEQUENCE COMPLETE ==")
    except Exception as e:
        logger.error(f"Critical failure in scraping sequence: {e}", exc_info=True)


def reporting_sequence():
    """Worker 2: The Reporting Task"""
    logger.info("== ALARM TRIGGERED: GENERATING CLIENT DELIVERABLE ==")
    try:
        generate_lead_report()
        logger.info("== DELIVERABLE GENERATED SUCCESSFULLY ==")
    except Exception as e:
        logger.error(f"Critical failure in reporting sequence: {e}", exc_info=True)


def main():
    init_vault()
    scheduler = BlockingScheduler()

    scheduler.add_job(
        scraping_sequence,
        trigger=IntervalTrigger(minutes=5),
        id="lead_scraper_worker",
        name="B2B Lead Scraper",
        replace_existing=True,
    )

    scheduler.add_job(
        reporting_sequence,
        trigger=CronTrigger(hour=17, minute=0),
        id="lead_reporter_worker",
        name="End of Day Lead Reporter",
        replace_existing=True,
    )

    try:
        active_jobs = len(scheduler.get_jobs())
        logger.info("==================================================")
        logger.info(f"== MASTER ENGINE ONLINE: {active_jobs} MODULES LOADED ==")
        logger.info("==================================================")
        logger.info("Scheduler active. Entering autonomous mode.")
        logger.info("Press Ctrl+C to safely terminate the system.")
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Admin override detected. Shutting down Master Engine gracefully.")


if __name__ == "__main__":
    main()

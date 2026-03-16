from playwright.sync_api import sync_playwright
import logging
from lead_vault import upsert_lead

logger = logging.getLogger(__name__)


class B2BLeadExtractor:
    def __init__(self, target_url):
        self.target_url = target_url
        self.total_leads_secured = 0

    def extract_directory(self):
        """
        Deploys the ghost browser to navigate the directory and extract business leads.
        """
        logger.info(f"Deploying ghost browser to: {self.target_url}")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            try:
                page.goto(self.target_url, timeout=60000, wait_until="domcontentloaded")
                logger.info("Scanning for business cards on the page...")

                page.wait_for_selector("div.business-card", timeout=10000)
                cards = page.locator("div.business-card")
                cards_count = cards.count()

                logger.info(f"Breach successful! Located {cards_count} potential leads.")

                for i in range(cards_count):
                    single_card = cards.nth(i)
                    try:
                        name = single_card.locator("h2.business-name").inner_text().strip()
                        website = single_card.locator("a.website-link").get_attribute("href")
                        phone = single_card.locator("span.phone-number").inner_text().strip()

                        upsert_lead(business_name=name, website=website, phone=phone)
                        self.total_leads_secured += 1

                    except Exception as e:
                        logger.warning(f"Incomplete data on card {i + 1}, skipping. Details: {e}")
                logger.info(
                    f"Extraction cycle complete. {self.total_leads_secured} leads processed."
                )

            except Exception as e:
                logger.error(f"Critical failure during extraction phase: {e}", exc_info=True)
            finally:
                browser.close()
                logger.info("Ghost browser connection severed.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    dummy_target = "https://scrapethissite.com/pages/"
    lead_engine = B2BLeadExtractor(target_url=dummy_target)
    lead_engine.extract_directory()

from playwright.sync_api import sync_playwright


def breach_hacker_news():
    print("Deploying ghost browser to hacker news...\n")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("Navigating to the target zone...")
        page.goto("https://news.ycombinator.com/", timeout=60000, wait_until="domcontentloaded")
        print("Scanning the article rows...")
        page.wait_for_selector("tr.athing")
        article_rows = page.query_selector_all("tr.athing")
        print(f"Breach successful! Found {len(article_rows)} articles on the front page.\n")
        for index, row in enumerate(article_rows[:10], 1):
            title_element = row.query_selector("span.titleline > a")
            if title_element:
                title = title_element.inner_text()
                link = title_element.get_attribute("href")
                print(f"{index}. {title}")
                print(f"    URL: {link}\n")

        print("Mission accomplished. Shutting down.")


if __name__ == "__main__":
    breach_hacker_news()

from playwright.sync_api import sync_playwright


def scrape_while_logged_in():
    print("Deploying ghost browser with VIP wristband...\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        print("Loading the auth.json session...")
        context = browser.new_context(storage_state="auth.json")
        page = context.new_page()

        print("Walking straight through the front door...")
        page.goto("http://quotes.toscrape.com/", timeout=60000, wait_until="domcontentloaded")
        print("Checking if the server recognizes us...")

        try:
            page.wait_for_selector("a[href='/logout']", timeout=5000)
            print("✅ Success! The server recognized our VIP wristband. No password needed.")
        except Exception as e:
            print(f"❌ Intruder alert! The server bounced us. Reason: {e}")

        page.wait_for_timeout(3000)
        print("Shutting down connection.")
        browser.close()


if __name__ == "__main__":
    scrape_while_logged_in()

from playwright.sync_api import sync_playwright


def login_and_save_session():
    print("\nDeploying ghost browser for infiltration...\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("Navigating to the login gate...")
        page.goto("http://quotes.toscrape.com/login", timeout=60000, wait_until="domcontentloaded")

        print("Injecting credentials")
        page.fill("input#username", "excel_admin")
        page.fill("input#password", "supersecret123")

        print("Pressing login...")
        page.click("input[type='submit']")

        print("Waiting for server confirmation...")
        page.wait_for_selector("a[href='/logout']")

        print("\nAccess Granted! We are inside.")
        print("Extracting the digital VIP wristband...")
        context.storage_state(path="auth.json")
        # page.wait_for_timeout(3000)
        print("Session saved successfully, Shutting down connection.")
        browser.close()


if __name__ == "__main__":
    login_and_save_session()

import requests
from bs4 import BeautifulSoup


class LeadExtractor:
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        self.session = requests.Session()  # A session keeps our connection alive and holds cookies

    def fetch_page(self):
        print(f"Fetching: {self.base_url}")
        try:
            response = self.session.get(self.base_url, headers=self.headers, timeout=10)
            response.raise_for_status()  # 404:page not found|403:forbidden|500: server error
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Connection failed: {e}")
            return None

    def extract_data(self):
        html_content = self.fetch_page()

        if not html_content:
            print("No data to parse.")
            return

        print("Parsing the data...\n")

        soup = BeautifulSoup(html_content, "html.parser")

        articles = soup.find_all("tr", class_="athing", limit=5)
        for article in articles:
            title_tag = soup.find("span", class_="titleline").find("a")
            title = title_tag.getText()
            link = title_tag.get("href")
            print(f"Title: {title}")
            print(f"Link: {link}")
            print("-" * 40)


if __name__ == "__main__":
    target_site = "https://news.ycombinator.com/"
    my_scraper = LeadExtractor(target_site)

    my_scraper.extract_data()

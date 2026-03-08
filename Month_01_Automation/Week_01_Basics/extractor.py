import csv
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
        print(f"\nFetching: {self.base_url}")
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
            return []  # Return an empty list if t he fetching failed

        print("Parsing the data...\n")
        soup = BeautifulSoup(html_content, "html.parser")

        extracted_leads = []

        articles = soup.find_all("tr", class_="athing", limit=5)
        for article in articles:
            title_tag = soup.find("span", class_="titleline").find("a")
            title = title_tag.getText()
            link = title_tag.get("href")

            lead_data = {"Title": title, "Link": link}
            extracted_leads.append(lead_data)
        return extracted_leads

    def save_to_csv(self, data, filename="leads.csv"):
        if not data:
            print("No data to save!")
            return
        print(f"Saving {len(data)} leads to {filename}...")
        column_headers = ["Title", "Link"]
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=column_headers)
            writer.writeheader()
            writer.writerows(data)
        print("Save Complete!!!")


if __name__ == "__main__":
    target_site = "https://news.ycombinator.com/"
    my_scraper = LeadExtractor(target_site)

    scraped_data = my_scraper.extract_data()
    my_scraper.save_to_csv(scraped_data, "hacker_news_leads.csv")

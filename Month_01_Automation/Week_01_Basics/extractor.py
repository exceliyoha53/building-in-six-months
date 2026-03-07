import requests


class LeadExtractor:
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        self.session = requests.session()  # A session keeps our connection alive and holds cookies

    def check_connection(self):
        print(f"Attempting to connect to {self.base_url}")
        try:
            response = self.session.get(self.base_url, headers=self.headers, timeout=10)
            response.raise_for_status()  # 404:page not found|403:forbidden|500: server error
            print(f"Success! status code: {response.status_code}")
            return True
        except requests.exceptions.RequestException as e:
            print(f"Connection failed: {e}")
            return False


if __name__ == "__main__":
    target_site = "https://www.google.com"
    my_scraper = LeadExtractor(target_site)
    my_scraper.check_connection()

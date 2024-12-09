from abc import ABC, abstractmethod
import requests
import time

class NewsSourceScraper(ABC):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.rate_limit = 1  # seconds between requests

    @abstractmethod
    def scrape_category(self, category):
        """Each news source must implement this method"""
        pass

    def _make_request(self, url, params=None):
        """Make HTTP request with rate limiting"""
        time.sleep(self.rate_limit)
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"Error making request to {url}: {e}")
            return None 
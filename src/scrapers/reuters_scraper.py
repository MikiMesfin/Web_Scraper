from .base_scraper import NewsSourceScraper
import feedparser

class ReutersScraper(NewsSourceScraper):
    def __init__(self):
        super().__init__()
        self.rss_feeds = {
            'world': 'https://www.reuters.com/world/rss',
            'business': 'https://www.reuters.com/business/rss',
            'technology': 'https://www.reuters.com/technology/rss',
            'sport': 'https://www.reuters.com/sports/rss',
            'environment': 'https://www.reuters.com/business/environment/rss'
        }

    def scrape_category(self, category):
        if category not in self.rss_feeds:
            return []
        
        print(f"Fetching RSS feed for {category}...")
        feed = feedparser.parse(self.rss_feeds[category])
        
        articles = []
        for entry in feed.entries:
            articles.append({
                'source': 'Reuters',
                'title': entry.title,
                'link': entry.link,
                'category': category,
                'timestamp': entry.published,
                'author': entry.get('author', 'Unknown'),
                'content': entry.get('summary', ''),
                'word_count': len(entry.get('summary', '').split()),
                'thumbnail': '',
                'last_modified': entry.get('updated', '')
            })
        
        return articles 
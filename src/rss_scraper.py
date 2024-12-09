import feedparser
import time

class ReutersRSSScraper:
    def __init__(self):
        self.rss_feeds = {
            'world': 'https://www.reutersagency.com/feed/?best-topics=world&post_type=best',
            'business': 'https://www.reutersagency.com/feed/?best-topics=business-finance&post_type=best',
            'technology': 'https://www.reutersagency.com/feed/?best-topics=tech&post_type=best'
        }

    def scrape_category(self, category):
        """Scrape articles from category RSS feed"""
        if category not in self.rss_feeds:
            return []
        
        print(f"Fetching RSS feed for {category}...")
        feed = feedparser.parse(self.rss_feeds[category])
        
        if not feed.entries:
            print(f"No entries found in {category} feed")
            return []
            
        articles = []
        for entry in feed.entries:
            articles.append({
                'title': entry.title,
                'link': entry.link,
                'category': category,
                'timestamp': entry.published
            })
            
        return articles 
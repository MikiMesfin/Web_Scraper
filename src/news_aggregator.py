from .scrapers.guardian_scraper import GuardianScraper
from .scrapers.nyt_scraper import NYTScraper
from .scrapers.reuters_scraper import ReutersScraper

class NewsAggregator:
    def __init__(self, config):
        self.scrapers = []
        
        if config.get('guardian_enabled', True):
            self.scrapers.append(GuardianScraper(config.get('guardian_api_key', 'test')))
            
        if config.get('nyt_enabled') and config.get('nyt_api_key'):
            self.scrapers.append(NYTScraper(config.get('nyt_api_key')))
            
        if config.get('reuters_enabled', True):
            self.scrapers.append(ReutersScraper())

    def scrape_all_sources(self, category):
        """Scrape articles from all configured sources"""
        all_articles = []
        
        for scraper in self.scrapers:
            try:
                articles = scraper.scrape_category(category)
                all_articles.extend(articles)
                print(f"Found {len(articles)} articles from {scraper.__class__.__name__}")
            except Exception as e:
                print(f"Error with {scraper.__class__.__name__}: {e}")
                continue
                
        return all_articles 

    def get_article_statistics(self, articles):
        """Calculate statistics for the articles"""
        if not articles:
            return {}
        
        word_counts = [int(article['word_count']) for article in articles if article['word_count']]
        return {
            'total_articles': len(articles),
            'average_word_count': sum(word_counts) / len(word_counts) if word_counts else 0,
            'authors': len(set(article['author'] for article in articles)),
            'earliest_article': min(articles, key=lambda x: x['timestamp'])['timestamp'],
            'latest_article': max(articles, key=lambda x: x['timestamp'])['timestamp']
        } 
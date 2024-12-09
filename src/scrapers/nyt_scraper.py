from .base_scraper import NewsSourceScraper

class NYTScraper(NewsSourceScraper):
    def __init__(self, api_key):
        super().__init__()
        self.base_url = "https://api.nytimes.com/svc/news/v3/content/all"
        self.api_key = api_key
        self.sections = {
            'world': 'world',
            'business': 'business',
            'technology': 'technology',
            'sports': 'sports',
            'arts': 'arts',
            'climate': 'climate'
        }

    def scrape_category(self, category):
        if category not in self.sections:
            return []
        
        params = {
            'api-key': self.api_key,
            'section': self.sections[category]
        }
        
        response = self._make_request(f"{self.base_url}/{self.sections[category]}.json", params)
        if not response:
            return []
            
        data = response.json()
        if 'results' not in data:
            return []
            
        articles = []
        for article in data['results']:
            articles.append({
                'source': 'New York Times',
                'title': article.get('title', ''),
                'link': article.get('url', ''),
                'category': category,
                'timestamp': article.get('published_date', ''),
                'author': article.get('byline', 'Unknown'),
                'content': article.get('abstract', ''),
                'word_count': len(article.get('abstract', '').split()),
                'thumbnail': article.get('multimedia', [{}])[0].get('url', '')
            })
        
        return articles 
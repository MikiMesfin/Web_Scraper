from .base_scraper import NewsSourceScraper

class GuardianScraper(NewsSourceScraper):
    def __init__(self, api_key="test"):
        super().__init__()
        self.base_url = "https://content.guardianapis.com/search"
        self.api_key = api_key
        self.sections = {
            'world': 'world',
            'business': 'business',
            'technology': 'technology',
            'sport': 'sport',
            'culture': 'culture',
            'environment': 'environment'
        }

    def scrape_category(self, category):
        if category not in self.sections:
            return []
        
        params = {
            'api-key': self.api_key,
            'section': self.sections[category],
            'show-fields': 'headline,shortUrl,bodyText,thumbnail,wordcount,byline,lastModified',
            'page-size': 50,
            'order-by': 'newest'
        }
        
        response = self._make_request(self.base_url, params)
        if not response:
            return []
            
        data = response.json()
        if 'response' not in data or 'results' not in data['response']:
            return []
            
        articles = []
        for article in data['response']['results']:
            fields = article.get('fields', {})
            articles.append({
                'source': 'The Guardian',
                'title': article['webTitle'],
                'link': article['webUrl'],
                'category': category,
                'timestamp': article['webPublicationDate'],
                'author': fields.get('byline', 'Unknown'),
                'content': fields.get('bodyText', ''),
                'word_count': fields.get('wordcount', 0),
                'thumbnail': fields.get('thumbnail', '')
            })
        
        return articles 
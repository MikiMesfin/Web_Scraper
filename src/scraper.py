import os
import requests
import time
from datetime import datetime, timedelta

class NewsScraper:
    def __init__(self):
        self.base_url = "https://content.guardianapis.com/search"
        self.api_key = "test"  # The Guardian's test API key
        self.sections = {
            'world': 'world',
            'business': 'business',
            'technology': 'technology',
            'sport': 'sport',
            'culture': 'culture',
            'environment': 'environment'
        }

    def scrape_category(self, category):
        """Scrape articles from The Guardian API with enhanced content"""
        if category not in self.sections:
            return []
        
        print(f"Fetching articles for {category}...")
        
        params = {
            'api-key': self.api_key,
            'section': self.sections[category],
            'show-fields': 'headline,shortUrl,bodyText,thumbnail,wordcount,byline,lastModified',
            'page-size': 50,
            'order-by': 'newest'
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if 'response' not in data or 'results' not in data['response']:
                print(f"No entries found in {category}")
                return []
                
            articles = []
            for article in data['response']['results']:
                fields = article.get('fields', {})
                articles.append({
                    'title': article['webTitle'],
                    'link': article['webUrl'],
                    'category': category,
                    'timestamp': article['webPublicationDate'],
                    'author': fields.get('byline', 'Unknown'),
                    'content': fields.get('bodyText', ''),
                    'word_count': fields.get('wordcount', 0),
                    'thumbnail': fields.get('thumbnail', ''),
                    'last_modified': fields.get('lastModified', ''),
                    'section_id': article.get('sectionId', ''),
                    'pillar_name': article.get('pillarName', '')
                })
            
            return articles
            
        except requests.RequestException as e:
            print(f"Error fetching articles: {e}")
            return []

    def fetch_webpage(self, url):
        """Fetch webpage content"""
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            # Add debug printing
            print(f"Status Code: {response.status_code}")
            print(f"Content Length: {len(response.text)}")
            print("First 500 characters of response:")
            print(response.text[:500])
            
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching the webpage: {e}")
            return None

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

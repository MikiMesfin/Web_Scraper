from src.news_aggregator import NewsAggregator
from src.utils import save_to_csv, save_statistics, generate_filename
from src.text_processor import TextProcessor
from src.visualizer import DataVisualizer
import time

def main():
    # Configuration
    config = {
        'guardian_enabled': True,
        'guardian_api_key': 'test',
        'nyt_enabled': True,
        'nyt_api_key': 'your_nyt_api_key',  # Add your NYT API key
        'reuters_enabled': True
    }

    # Initialize components
    aggregator = NewsAggregator(config)
    processor = TextProcessor()
    visualizer = DataVisualizer()
    
    # Define categories and filters
    categories = ['world', 'business', 'technology', 'sport', 'culture', 'environment']
    keywords = ['climate', 'innovation', 'economy']  # Adjust these
    exclude = ['gossip', 'rumor']  # Adjust these
    min_words = 200  # Adjust this
    
    all_articles = []
    category_stats = {}
    
    # Scrape and process articles
    for category in categories:
        try:
            print(f"\nScraping {category} news...")
            articles = aggregator.scrape_all_sources(category)
            
            if articles:
                # Filter articles
                filtered_articles = processor.filter_content(
                    articles, 
                    keywords=keywords,
                    exclude=exclude,
                    min_words=min_words
                )
                
                # Add summaries
                for article in filtered_articles:
                    article['summary'] = processor.summarize_text(article['content'])
                
                all_articles.extend(filtered_articles)
                print(f"Found {len(filtered_articles)} matching articles in {category}")
                
                # Generate and save statistics
                stats = aggregator.get_article_statistics(filtered_articles)
                category_stats[category] = stats
                
            time.sleep(1)
        except Exception as e:
            print(f"Error processing {category}: {e}")
            continue
    
    # Save and visualize results
    if all_articles:
        try:
            # Save articles
            filename = generate_filename()
            filepath = save_to_csv(all_articles, filename)
            print(f"\nSaved {len(all_articles)} articles to {filepath}")
            
            # Create visualizations
            print("\nGenerating visualizations...")
            cat_dist = visualizer.create_category_distribution(all_articles)
            word_dist = visualizer.create_word_count_distribution(all_articles)
            timeline = visualizer.create_publication_timeline(all_articles)
            
            print(f"Created visualizations:")
            print(f"- Category distribution: {cat_dist}")
            print(f"- Word count distribution: {word_dist}")
            print(f"- Publication timeline: {timeline}")
            
        except Exception as e:
            print(f"Error saving/visualizing results: {e}")
    else:
        print("No articles found")

if __name__ == "__main__":
    main()

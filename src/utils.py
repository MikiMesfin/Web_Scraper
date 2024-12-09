import os
import csv
import json
from datetime import datetime

def create_data_directory():
    """Create data directory if it doesn't exist"""
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    return data_dir

def save_to_csv(articles, filename):
    """Save articles to CSV file"""
    data_dir = create_data_directory()
    filepath = os.path.join(data_dir, filename)
    
    fieldnames = [
        'source', 'title', 'link', 'category', 'timestamp', 'author', 
        'content', 'word_count', 'thumbnail', 'last_modified',
        'section_id', 'pillar_name', 'summary'
    ]
    
    with open(filepath, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(articles)
    return filepath

def save_statistics(stats, category):
    """Save statistics to JSON file"""
    data_dir = create_data_directory()
    filename = f'statistics_{category}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    filepath = os.path.join(data_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(stats, file, indent=4)
    return filepath

def generate_filename():
    """Generate filename with timestamp"""
    return f'guardian_articles_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'

import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import pandas as pd
import os

class DataVisualizer:
    def __init__(self):
        self.output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'visualizations')
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def create_category_distribution(self, articles):
        """Create pie chart of articles by category"""
        plt.figure(figsize=(10, 8))
        df = pd.DataFrame(articles)
        category_counts = df['category'].value_counts()
        
        plt.pie(category_counts.values, labels=category_counts.index, autopct='%1.1f%%')
        plt.title('Article Distribution by Category')
        
        filename = f'category_distribution_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
        plt.savefig(os.path.join(self.output_dir, filename))
        plt.close()
        return filename

    def create_word_count_distribution(self, articles):
        """Create histogram of word counts"""
        plt.figure(figsize=(12, 6))
        df = pd.DataFrame(articles)
        
        sns.histplot(data=df, x='word_count', hue='category', multiple="stack")
        plt.title('Word Count Distribution by Category')
        plt.xlabel('Word Count')
        plt.ylabel('Number of Articles')
        
        filename = f'word_count_distribution_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
        plt.savefig(os.path.join(self.output_dir, filename))
        plt.close()
        return filename

    def create_publication_timeline(self, articles):
        """Create timeline of article publications"""
        plt.figure(figsize=(15, 6))
        df = pd.DataFrame(articles)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        timeline = df.groupby(['timestamp', 'category']).size().unstack(fill_value=0)
        timeline.plot(kind='area', stacked=True)
        
        plt.title('Publication Timeline by Category')
        plt.xlabel('Publication Date')
        plt.ylabel('Number of Articles')
        
        filename = f'publication_timeline_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
        plt.savefig(os.path.join(self.output_dir, filename))
        plt.close()
        return filename 
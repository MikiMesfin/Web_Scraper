from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import nltk
import os

class TextProcessor:
    def __init__(self):
        # Set NLTK data path
        home = os.path.expanduser("~")
        nltk.data.path.append(os.path.join(home, "nltk_data"))
        
        try:
            self.stop_words = set(stopwords.words('english'))
        except LookupError:
            print("Warning: stopwords not found. Using empty set.")
            self.stop_words = set()

    def summarize_text(self, text, num_sentences=3):
        """Generate a summary of the text"""
        if not text:
            return ""
            
        # Tokenize the text into sentences
        sentences = sent_tokenize(text)
        if len(sentences) <= num_sentences:
            return text
            
        # Calculate word frequency
        word_freq = {}
        for word in word_tokenize(text.lower()):
            if word not in self.stop_words and word.isalnum():
                word_freq[word] = word_freq.get(word, 0) + 1
                
        # Calculate sentence scores
        sentence_scores = {}
        for sentence in sentences:
            for word in word_tokenize(sentence.lower()):
                if word in word_freq:
                    sentence_scores[sentence] = sentence_scores.get(sentence, 0) + word_freq[word]
                    
        # Get top sentences
        summary_sentences = sorted(sentence_scores.items(), 
                                key=lambda x: x[1], 
                                reverse=True)[:num_sentences]
        
        # Maintain original order of sentences
        summary = [s[0] for s in sorted(summary_sentences, 
                                      key=lambda x: sentences.index(x[0]))]
        
        return ' '.join(summary)

    def filter_content(self, articles, keywords=None, exclude=None, min_words=None):
        """Filter articles based on keywords and criteria"""
        if not articles:
            return []
            
        filtered_articles = articles.copy()
        
        if keywords:
            keywords = [k.lower() for k in keywords]
            filtered_articles = [
                article for article in filtered_articles
                if any(k in article['title'].lower() or k in article['content'].lower() 
                      for k in keywords)
            ]
            
        if exclude:
            exclude = [e.lower() for e in exclude]
            filtered_articles = [
                article for article in filtered_articles
                if not any(e in article['title'].lower() or e in article['content'].lower() 
                          for e in exclude)
            ]
            
        if min_words:
            filtered_articles = [
                article for article in filtered_articles
                if int(article['word_count']) >= min_words
            ]
            
        return filtered_articles 
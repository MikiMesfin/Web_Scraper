import ssl
import nltk
import os

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

def download_nltk_data():
    """Download required NLTK data with SSL verification disabled"""
    try:
        # Create nltk_data directory in user's home
        home = os.path.expanduser("~")
        nltk_data_dir = os.path.join(home, "nltk_data")
        if not os.path.exists(nltk_data_dir):
            os.makedirs(nltk_data_dir)

        print("Downloading NLTK data...")
        nltk.download('punkt', download_dir=nltk_data_dir)
        nltk.download('stopwords', download_dir=nltk_data_dir)
        print("NLTK data downloaded successfully!")
    except Exception as e:
        print(f"Error downloading NLTK data: {e}")

if __name__ == "__main__":
    download_nltk_data() 
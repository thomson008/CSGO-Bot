
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()

def is_negative(message):
    print(f'Analysis for "{message}": {sia.polarity_scores(message)}')
    return sia.polarity_scores(message)['compound'] < 0
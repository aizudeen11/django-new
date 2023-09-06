from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
sia = SentimentIntensityAnalyzer()
test = sia.polarity_scores('fk u')
print(test)
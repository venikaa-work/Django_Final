from nltk.sentiment.vader import SentimentIntensityAnalyzer

class SentimentModel:
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()

    def analyze(self, conversation):
        return self.sia.polarity_scores(conversation)

# Create an instance of the sentiment model
sentiment_model = SentimentModel()

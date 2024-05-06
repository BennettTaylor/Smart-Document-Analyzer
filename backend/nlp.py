from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import en_core_web_sm
from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
nlp = en_core_web_sm.load()
sentimentAnalyser = SentimentIntensityAnalyzer()


def perform_nlp(text):
    sentiment_scores = sentimentAnalyser.polarity_scores(text)
    sentiment = sentiment_scores['compound']
    doc = nlp(text)
    keywords = doc.ents
    return sentiment, keywords


def generate_summary(text):
    summary = summarizer(text, max_length=130, min_length=30)
    summary = summary[0]['summary_text']
    return summary
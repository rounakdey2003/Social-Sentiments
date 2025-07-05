from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import numpy as np

class SentimentEngine:
    def __init__(self):
        self.vader_analyzer = SentimentIntensityAnalyzer()
    
    def analyze_sentiment(self, text):
        if not text or text.strip() == "":
            return {
                'label': 'Neutral',
                'score': 0.0,
                'positive': 0.0,
                'negative': 0.0,
                'neutral': 1.0,
                'compound': 0.0
            }
        
        cleaned_text = self._clean_text(text)
        
        vader_scores = self.vader_analyzer.polarity_scores(cleaned_text)
        
        blob = TextBlob(cleaned_text)
        textblob_polarity = blob.sentiment.polarity
        textblob_subjectivity = blob.sentiment.subjectivity
        
        combined_sentiment = self._combine_sentiments(vader_scores, textblob_polarity)
        
        return combined_sentiment
    
    def _clean_text(self, text):
        import re
        
        text = re.sub(r'http\S+|www.\S+', '', text)
                
        text = re.sub(r'@\w+|#\w+', '', text)
                
        text = ' '.join(text.split())
        
        return text
    
    def _combine_sentiments(self, vader_scores, textblob_polarity):        
                
        textblob_normalized = textblob_polarity
                
        vader_weight = 0.7
        textblob_weight = 0.3
        
        combined_compound = (vader_scores['compound'] * vader_weight + 
                           textblob_normalized * textblob_weight)
                
        if combined_compound >= 0.05:
            label = 'Positive'
        elif combined_compound <= -0.05:
            label = 'Negative'
        else:
            label = 'Neutral'
                
        confidence = abs(combined_compound)
        
        return {
            'label': label,
            'score': confidence,
            'positive': vader_scores['pos'],
            'negative': vader_scores['neg'],
            'neutral': vader_scores['neu'],
            'compound': combined_compound,
            'textblob_polarity': textblob_polarity
        }
    
    def batch_analyze(self, texts):        
        results = []
        for text in texts:
            results.append(self.analyze_sentiment(text))
        return results
    
    def get_sentiment_summary(self, sentiments):        
        if not sentiments:
            return {}
        
        labels = [s['label'] for s in sentiments]
        scores = [s['score'] for s in sentiments]
        compounds = [s['compound'] for s in sentiments]
        
        summary = {
            'total_count': len(sentiments),
            'positive_count': labels.count('Positive'),
            'negative_count': labels.count('Negative'),
            'neutral_count': labels.count('Neutral'),
            'average_score': np.mean(scores),
            'average_compound': np.mean(compounds),
            'sentiment_distribution': {
                'positive_ratio': labels.count('Positive') / len(labels),
                'negative_ratio': labels.count('Negative') / len(labels),
                'neutral_ratio': labels.count('Neutral') / len(labels)
            }
        }
        
        return summary

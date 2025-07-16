import numpy as np
import re

def simple_sentiment_score(text):
    """
    Assign a sentiment score based on keywords.
    Args:
        text (str): News headline or text.
    Returns:
        float: Sentiment score (-1 to 1).
    """
    positive_words = ['beat', 'growth', 'boost', 'gain', 'up', 'positive', 'record']
    negative_words = ['volatility', 'regulatory', 'loss', 'down', 'negative', 'crash']
    score = 0
    for word in positive_words:
        if re.search(rf'\\b{word}\\b', text, re.IGNORECASE):
            score += 1
    for word in negative_words:
        if re.search(rf'\\b{word}\\b', text, re.IGNORECASE):
            score -= 1
    return np.tanh(score / 2)

def batch_sentiment_analysis(news_list):
    """
    Analyze sentiment for a list of news headlines.
    Args:
        news_list (list): List of dicts with 'headline' key.
    Returns:
        list: List of dicts with 'headline' and 'score'.
    """
    results = []
    for item in news_list:
        headline = item.get('headline', '')
        score = simple_sentiment_score(headline)
        results.append({'headline': headline, 'score': score})
    return results 
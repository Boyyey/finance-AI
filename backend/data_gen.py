import numpy as np
import pandas as pd
import random

def generate_synthetic_data():
    # Synthetic financials
    financials = {
        'revenue': np.random.randint(100000, 1000000),
        'expenses': np.random.randint(50000, 900000),
        'net_income': np.random.randint(10000, 100000)
    }
    # Synthetic stock prices
    prices = list(np.cumsum(np.random.normal(0, 1, 30)) + 100)
    # Synthetic news
    news = [
        {'headline': random.choice([
            'Company X beats earnings expectations',
            'Market volatility increases',
            'New product launch boosts stock',
            'Regulatory changes impact sector',
            'Analysts predict growth'])}
        for _ in range(5)
    ]
    # Synthetic assets
    assets = ['AAPL', 'GOOG', 'TSLA']
    return {'financials': financials, 'prices': prices, 'news': news, 'assets': assets} 
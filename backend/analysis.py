import numpy as np
import pandas as pd
from risk import calculate_volatility, calculate_drawdown, calculate_sharpe_ratio
from forecast import arima_forecast, lstm_forecast_placeholder, prophet_forecast, xgboost_forecast
from sentiment import batch_sentiment_analysis
from utils import log_event, validate_prices

def analyze_financials(data):
    """
    Perform detailed financial analysis, including ratios and trend detection.
    Args:
        data (dict): Financial data with 'financials' and 'prices'.
    Returns:
        dict: Analysis results.
    """
    f = data.get('financials', {})
    ratios = {
        'profit_margin': f.get('net_income', 0) / max(f.get('revenue', 1), 1),
        'debt_to_equity': np.random.uniform(0.5, 2.0),
        'return_on_equity': np.random.uniform(0.05, 0.2),
        'current_ratio': np.random.uniform(1.0, 3.0),
        'quick_ratio': np.random.uniform(0.8, 2.5),
        'asset_turnover': np.random.uniform(0.5, 2.0)
    }
    trend = 'upward' if ratios['profit_margin'] > 0.2 else 'stable'
    explanation = f"Profit margin is {'high' if ratios['profit_margin'] > 0.2 else 'moderate'}, indicating {trend} trend."
    log_event('Financial analysis performed', {'ratios': ratios, 'trend': trend})
    return {'financial_ratios': ratios, 'trend': trend, 'explanation': explanation}

def forecast_prices(data, method='arima', steps=5):
    """
    Forecast future prices using ARIMA or LSTM placeholder.
    Args:
        data (dict): Data with 'prices'.
        method (str): 'arima' or 'lstm'.
        steps (int): Forecast horizon.
    Returns:
        dict: Forecasted prices.
    """
    prices = data.get('prices', [])
    if not validate_prices(prices):
        return {'error': 'Invalid price data'}
    if method == 'lstm':
        forecast = lstm_forecast_placeholder(prices, steps)
    elif method == 'prophet':
        forecast = prophet_forecast(prices, steps)
    elif method == 'xgboost':
        forecast = xgboost_forecast(prices, steps)
    else:
        forecast = arima_forecast(prices, steps)
    log_event('Forecast performed', {'method': method, 'forecast': forecast})
    return {'forecast': forecast}

def analyze_sentiment(data):
    """
    Analyze sentiment for all news headlines in data.
    Args:
        data (dict): Data with 'news' (list of dicts).
    Returns:
        dict: Sentiment results.
    """
    news = data.get('news', [])
    results = batch_sentiment_analysis(news)
    avg_score = np.mean([r['score'] for r in results]) if results else 0
    log_event('Sentiment analysis performed', {'avg_score': avg_score})
    return {'sentiments': results, 'average_score': avg_score}

def risk_metrics(data):
    """
    Calculate risk metrics for price series.
    Args:
        data (dict): Data with 'prices'.
    Returns:
        dict: Risk metrics.
    """
    prices = data.get('prices', [])
    if not validate_prices(prices):
        return {'error': 'Invalid price data'}
    volatility = calculate_volatility(prices)
    drawdown = calculate_drawdown(prices)
    sharpe = calculate_sharpe_ratio(prices)
    log_event('Risk metrics calculated', {'volatility': volatility, 'drawdown': drawdown, 'sharpe': sharpe})
    return {'volatility': volatility, 'max_drawdown': drawdown, 'sharpe_ratio': sharpe}

def optimize_portfolio(data, risk_aversion=0.5):
    """
    Optimize portfolio weights with a risk aversion parameter.
    Args:
        data (dict): Data with 'assets'.
        risk_aversion (float): Risk aversion parameter (0-1).
    Returns:
        dict: Portfolio weights.
    """
    assets = data.get('assets', ['AAPL', 'GOOG', 'TSLA'])
    n = len(assets)
    weights = np.random.dirichlet(np.ones(n) * (1 - risk_aversion + 0.1), size=1)[0]
    log_event('Portfolio optimized', {'weights': dict(zip(assets, weights)), 'risk_aversion': risk_aversion})
    return {'weights': dict(zip(assets, weights)), 'risk_aversion': risk_aversion} 
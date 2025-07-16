import yfinance as yf
import requests
import datetime
import pandas as pd

NEWS_API_KEY = '3811bc6249ca464995c0d7b856231fc1'  # Replace with your NewsAPI key


def fetch_stock_data(ticker, period='1y', interval='1d'):
    """
    Fetch historical stock price data using yfinance.
    Args:
        ticker (str): Stock ticker symbol.
        period (str): Data period (e.g., '1y', '6mo').
        interval (str): Data interval (e.g., '1d', '1wk').
    Returns:
        dict: { 'prices': [...], 'dates': [...] }
    """
    try:
        data = yf.download(ticker, period=period, interval=interval, progress=False)
        if data is None or data.empty:
            return {'error': 'No data returned for ticker.'}
        prices = data['Close']
        if isinstance(prices, pd.DataFrame):
            prices = prices.iloc[:, 0]
        prices = prices.dropna().tolist()
        dates = [str(d.date()) for d in data.index]
        return {'prices': prices, 'dates': dates}
    except Exception as e:
        return {'error': str(e)}


def fetch_news(query='stock market', page_size=5):
    """
    Fetch latest news headlines using NewsAPI.
    Args:
        query (str): Search query.
        page_size (int): Number of articles.
    Returns:
        list: List of dicts with 'headline' and 'url'.
    """
    url = f'https://newsapi.org/v2/everything?q={query}&pageSize={page_size}&apiKey={NEWS_API_KEY}'
    try:
        resp = requests.get(url)
        articles = resp.json().get('articles', [])
        return [{'headline': a['title'], 'url': a['url']} for a in articles]
    except Exception as e:
        return [{'headline': f'Error: {e}', 'url': ''}] 
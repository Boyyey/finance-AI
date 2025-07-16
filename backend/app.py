from flask import Flask, request, jsonify
from analysis import analyze_financials, forecast_prices, analyze_sentiment, optimize_portfolio, risk_metrics
from data_gen import generate_synthetic_data
from utils import setup_logging
from data_sources import fetch_stock_data, fetch_news
from llm import summarize_text
from explain import explain_xgboost_forecast

app = Flask(__name__)
setup_logging()

@app.route('/generate-data', methods=['GET'])
def generate_data():
    """Generate synthetic financial data."""
    data = generate_synthetic_data()
    return jsonify(data)

@app.route('/stock', methods=['GET'])
def get_stock():
    """Fetch real stock data for a given ticker."""
    ticker = request.args.get('ticker', 'AAPL')
    period = request.args.get('period', '1y')
    interval = request.args.get('interval', '1d')
    data = fetch_stock_data(ticker, period, interval)
    return jsonify(data)

@app.route('/news', methods=['GET'])
def get_news():
    """Fetch real news headlines for a given query."""
    query = request.args.get('query', 'stock market')
    page_size = int(request.args.get('page_size', 5))
    data = fetch_news(query, page_size)
    return jsonify(data)

@app.route('/sec-filings', methods=['GET'])
def get_sec_filings():
    """Fetch SEC filings for a given ticker (placeholder)."""
    ticker = request.args.get('ticker', 'AAPL')
    # Placeholder: return dummy filings
    filings = [
        {'type': '10-K', 'date': '2023-03-01', 'url': 'https://www.sec.gov/Archives/edgar/data/0000320193/000032019323000010/0000320193-23-000010-index.htm'},
        {'type': '10-Q', 'date': '2023-06-01', 'url': 'https://www.sec.gov/Archives/edgar/data/0000320193/000032019323000011/0000320193-23-000011-index.htm'}
    ]
    return jsonify({'filings': filings})

@app.route('/analyze', methods=['POST'])
def analyze():
    """Perform financial analysis on provided data."""
    data = request.json
    result = analyze_financials(data)
    return jsonify(result)

@app.route('/forecast', methods=['POST'])
def forecast():
    """Forecast future prices using selected method."""
    data = request.json
    method = request.args.get('method', 'arima')
    steps = int(request.args.get('steps', 5))
    result = forecast_prices(data, method=method, steps=steps)
    return jsonify(result)

@app.route('/sentiment', methods=['POST'])
def sentiment():
    """Analyze sentiment of news headlines."""
    data = request.json
    result = analyze_sentiment(data)
    return jsonify(result)

@app.route('/risk', methods=['POST'])
def risk():
    """Calculate risk metrics for price series."""
    data = request.json
    result = risk_metrics(data)
    return jsonify(result)

@app.route('/optimize', methods=['POST'])
def optimize():
    """Optimize portfolio weights with risk aversion parameter."""
    data = request.json
    risk_aversion = float(request.args.get('risk_aversion', 0.5))
    result = optimize_portfolio(data, risk_aversion=risk_aversion)
    return jsonify(result)

@app.route('/summarize', methods=['POST'])
def summarize():
    """Summarize provided text using LLM."""
    data = request.json
    text = data.get('text', '') if data else ''
    summary = summarize_text(text)
    return jsonify({'summary': summary})

@app.route('/explain-forecast', methods=['POST'])
def explain_forecast():
    """Explain XGBoost forecast using SHAP and ELI5."""
    data = request.json
    prices = data.get('prices', []) if data else []
    steps = int(data.get('steps', 5)) if data else 5
    window = int(data.get('window', 5)) if data else 5
    result = explain_xgboost_forecast(prices, steps, window)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True) 
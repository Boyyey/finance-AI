import pytest
from backend.analysis import analyze_financials, forecast_prices, analyze_sentiment, risk_metrics, optimize_portfolio

def sample_data():
    return {
        'financials': {'revenue': 500000, 'expenses': 300000, 'net_income': 100000},
        'prices': [100, 102, 101, 105, 107, 110],
        'news': [{'headline': 'Company X beats earnings expectations'}, {'headline': 'Market volatility increases'}],
        'assets': ['AAPL', 'GOOG', 'TSLA']
    }

def test_analyze_financials():
    data = sample_data()
    result = analyze_financials(data)
    assert 'financial_ratios' in result
    assert 'trend' in result

def test_forecast_prices():
    data = sample_data()
    result = forecast_prices(data, method='arima', steps=3)
    assert 'forecast' in result
    assert len(result['forecast']) == 3

def test_analyze_sentiment():
    data = sample_data()
    result = analyze_sentiment(data)
    assert 'sentiments' in result
    assert isinstance(result['sentiments'], list)

def test_risk_metrics():
    data = sample_data()
    result = risk_metrics(data)
    assert 'volatility' in result
    assert 'max_drawdown' in result
    assert 'sharpe_ratio' in result

def test_optimize_portfolio():
    data = sample_data()
    result = optimize_portfolio(data, risk_aversion=0.5)
    assert 'weights' in result
    assert abs(sum(result['weights'].values()) - 1) < 1e-6 
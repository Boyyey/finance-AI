import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from prophet import Prophet
import xgboost as xgb

def arima_forecast(prices, steps=5):
    """
    Forecast future prices using ARIMA model.
    Args:
        prices (list or np.array): Historical prices.
        steps (int): Number of periods to forecast.
    Returns:
        list: Forecasted prices.
    """
    try:
        model = ARIMA(prices, order=(1,1,1))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=steps)
        return forecast.tolist()
    except Exception as e:
        return [float(prices[-1])] * steps

def lstm_forecast_placeholder(prices, steps=5):
    """
    Placeholder for LSTM-based forecasting. Returns random walk for now.
    Args:
        prices (list or np.array): Historical prices.
        steps (int): Number of periods to forecast.
    Returns:
        list: Forecasted prices.
    """
    last = prices[-1]
    return (np.cumsum(np.random.normal(0, 1, steps)) + last).tolist()

def prophet_forecast(prices, steps=5):
    """
    Forecast future prices using Prophet.
    Args:
        prices (list or np.array): Historical prices.
        steps (int): Number of periods to forecast.
    Returns:
        list: Forecasted prices.
    """
    try:
        df = pd.DataFrame({'ds': pd.date_range(start='2020-01-01', periods=len(prices), freq='D'), 'y': prices})
        model = Prophet()
        model.fit(df)
        future = model.make_future_dataframe(periods=steps)
        forecast = model.predict(future)
        return forecast['yhat'][-steps:].tolist()
    except Exception as e:
        return [float(prices[-1])] * steps

def xgboost_forecast(prices, steps=5, window=5):
    """
    Forecast future prices using XGBoost regression.
    Args:
        prices (list or np.array): Historical prices.
        steps (int): Number of periods to forecast.
        window (int): Window size for features.
    Returns:
        list: Forecasted prices.
    """
    try:
        X, y = [], []
        for i in range(len(prices) - window):
            X.append(prices[i:i+window])
            y.append(prices[i+window])
        X, y = np.array(X), np.array(y)
        model = xgb.XGBRegressor(objective='reg:squarederror')
        model.fit(X, y)
        last_window = prices[-window:]
        preds = []
        for _ in range(steps):
            pred = model.predict(np.array(last_window).reshape(1, -1))[0]
            preds.append(pred)
            last_window = np.append(last_window[1:], pred)
        return preds
    except Exception as e:
        return [float(prices[-1])] * steps 
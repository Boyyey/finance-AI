from backend.forecast import arima_forecast, lstm_forecast_placeholder

def test_arima_forecast():
    prices = [100, 102, 101, 105, 107, 110]
    forecast = arima_forecast(prices, steps=3)
    assert isinstance(forecast, list)
    assert len(forecast) == 3

def test_lstm_forecast_placeholder():
    prices = [100, 102, 101, 105, 107, 110]
    forecast = lstm_forecast_placeholder(prices, steps=3)
    assert isinstance(forecast, list)
    assert len(forecast) == 3 
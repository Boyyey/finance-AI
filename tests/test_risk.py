from backend.risk import calculate_volatility, calculate_drawdown, calculate_sharpe_ratio

def test_calculate_volatility():
    prices = [100, 102, 101, 105, 107, 110]
    vol = calculate_volatility(prices)
    assert isinstance(vol, float)
    assert vol >= 0

def test_calculate_drawdown():
    prices = [100, 102, 101, 105, 107, 110]
    dd = calculate_drawdown(prices)
    assert isinstance(dd, float)
    assert 0 <= dd <= 1

def test_calculate_sharpe_ratio():
    prices = [100, 102, 101, 105, 107, 110]
    sharpe = calculate_sharpe_ratio(prices)
    assert isinstance(sharpe, float) 
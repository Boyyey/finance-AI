import numpy as np
import pandas as pd

def calculate_volatility(prices):
    """
    Calculate annualized volatility of a price series.
    Args:
        prices (list or np.array): List of prices.
    Returns:
        float: Annualized volatility.
    """
    returns = np.diff(prices) / prices[:-1]
    volatility = np.std(returns) * np.sqrt(252)
    return float(volatility)

def calculate_drawdown(prices):
    """
    Calculate the maximum drawdown of a price series.
    Args:
        prices (list or np.array): List of prices.
    Returns:
        float: Maximum drawdown (as a positive number).
    """
    prices = np.array(prices)
    running_max = np.maximum.accumulate(prices)
    drawdowns = (running_max - prices) / running_max
    max_drawdown = np.max(drawdowns)
    return float(max_drawdown)

def calculate_sharpe_ratio(prices, risk_free_rate=0.01):
    """
    Calculate the Sharpe ratio of a price series.
    Args:
        prices (list or np.array): List of prices.
        risk_free_rate (float): Annual risk-free rate (default 0.01).
    Returns:
        float: Sharpe ratio.
    """
    returns = np.diff(prices) / prices[:-1]
    excess_returns = returns - (risk_free_rate / 252)
    sharpe = np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(252)
    return float(sharpe) 
import xgboost as xgb
import shap
import eli5
import numpy as np
import pandas as pd
# from eli5.sklearn import explain_prediction_df  # Unused, remove


def explain_xgboost_forecast(prices, steps=5, window=5):
    """
    Train XGBoost on price series and return SHAP values and ELI5 explanation for the last prediction.
    Args:
        prices (list): Historical prices.
        steps (int): Number of forecast steps.
        window (int): Feature window size.
    Returns:
        dict: SHAP values and ELI5 HTML explanation.
    """
    X, y = [], []
    for i in range(len(prices) - window):
        X.append(prices[i:i+window])
        y.append(prices[i+window])
    X, y = np.array(X), np.array(y)
    model = xgb.XGBRegressor(objective='reg:squarederror')
    model.fit(X, y)
    last_window = np.array(prices[-window:]).reshape(1, -1)
    # SHAP explanation
    explainer = shap.Explainer(model)
    shap_values = explainer(last_window)
    # ELI5 explanation
    try:
        explanation = eli5.explain_prediction(model, last_window[0], feature_names=[f'lag_{i+1}' for i in range(window)])
        html_str = eli5.format_as_html(explanation)
    except Exception as e:
        html_str = f'ELI5 explanation error: {e}'
    return {
        'shap_values': shap_values.values.tolist() if hasattr(shap_values, 'values') else [],
        'eli5_html': html_str
    } 
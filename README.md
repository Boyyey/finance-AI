# 💰 Autonomous Financial Analyst

Feed in financial reports, stock data, and market news to get in-depth analysis, risk metrics, and future forecasts. Optionally, optimize your portfolio!

---

## 🚀 Features
- In-depth financial report analysis
- Time-series forecasting (ARIMA, LSTM placeholder)
- Sentiment analysis (news impact)
- Risk metrics (volatility, Sharpe ratio, drawdown)
- Portfolio optimization (mean-variance, risk aversion)
- Modern, interactive dashboard
- Synthetic data for demo/testing
- CSV upload and result downloads

## 🧠 Stack
- **Backend:** Flask (Python)
- **Frontend:** Streamlit (Python)
- **ML/AI:** numpy, pandas, plotly, statsmodels, etc.

## 📦 Project Structure
```
MON-AI/
│
├── backend/
│   ├── app.py           # Flask API
│   ├── analysis.py      # Core analysis logic
│   ├── data_gen.py      # Synthetic data generation
│   ├── risk.py          # Risk metrics
│   ├── forecast.py      # Forecasting models
│   ├── sentiment.py     # Sentiment analysis
│   ├── utils.py         # Utilities
│   └── requirements.txt
│
├── dashboard/
│   ├── app.py           # Streamlit dashboard
│   └── requirements.txt
│
├── tests/               # Unit tests
│
└── README.md
```

## 🏁 Quickstart

### 1. Backend (Flask)
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### 2. Dashboard (Streamlit)
```bash
cd dashboard
pip install -r requirements.txt
streamlit run app.py
```

- The dashboard will connect to the backend at `http://localhost:5000` by default.

## 📝 API Documentation

### Endpoints
- `GET /generate-data` — Generate synthetic data
- `POST /analyze` — Financial analysis
- `POST /forecast?method=arima|lstm&steps=N` — Price forecasting
- `POST /sentiment` — Sentiment analysis
- `POST /risk` — Risk metrics
- `POST /optimize?risk_aversion=0.0-1.0` — Portfolio optimization

### Example Request (Python)
```python
import requests
r = requests.get('http://localhost:5000/generate-data')
data = r.json()
result = requests.post('http://localhost:5000/analyze', json=data).json()
print(result)
```

## 🧪 Running Tests
```bash
cd tests
pytest
```

## 🤝 Contributing
Pull requests welcome! Please add tests and docstrings for new features.

## 👤 Users
- Investors, hedge funds, retail traders

## 🔥 Utility
AI-powered investing on another level. Could beat the markets or warn of crashes.

---

Made with ❤️ using Python, Flask, and Streamlit. 
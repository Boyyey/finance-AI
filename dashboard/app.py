import streamlit as st
import streamlit.components.v1 as components
import requests
import pandas as pd
import plotly.graph_objs as go
import io
import json

BACKEND_URL = 'http://localhost:5000'

st.set_page_config(page_title='💰 Autonomous Financial Analyst', layout='wide')

# --- Sidebar ---
st.sidebar.header('Navigation')
page = st.sidebar.radio('Go to', ['Data', 'Analysis', 'Forecast', 'Sentiment', 'Risk', 'Portfolio', 'SEC Filings'])

st.sidebar.header('Data Source')
data_source = st.sidebar.selectbox('Data Source', ['Synthetic', 'Real'])

# --- Real Data Controls ---
if data_source == 'Real':
    st.sidebar.subheader('Stock Data')
    ticker = st.sidebar.text_input('Ticker', 'AAPL')
    period = st.sidebar.selectbox('Period', ['1y', '6mo', '3mo', '1mo'])
    interval = st.sidebar.selectbox('Interval', ['1d', '1wk', '1mo'])
    if st.sidebar.button('Fetch Stock Data'):
        r = requests.get(f'{BACKEND_URL}/stock', params={'ticker': ticker, 'period': period, 'interval': interval})
        if r.ok and 'prices' in r.json():
            st.session_state['data'] = {'prices': r.json()['prices'], 'dates': r.json()['dates'], 'assets': [ticker]}
            st.success(f'Loaded {ticker} stock data!')
        else:
            st.error(r.json().get('error', 'Failed to fetch stock data.'))
    st.sidebar.subheader('News Data')
    news_query = st.sidebar.text_input('News Query', 'stock market')
    news_count = st.sidebar.slider('Number of News', 1, 10, 5)
    if st.sidebar.button('Fetch News'):
        r = requests.get(f'{BACKEND_URL}/news', params={'query': news_query, 'page_size': news_count})
        if r.ok:
            st.session_state['news'] = r.json()
            st.success('Loaded news!')
        else:
            st.error('Failed to fetch news.')
    st.sidebar.subheader('SEC Filings')
    sec_ticker = st.sidebar.text_input('SEC Ticker', 'AAPL')
    if st.sidebar.button('Fetch SEC Filings'):
        r = requests.get(f'{BACKEND_URL}/sec-filings', params={'ticker': sec_ticker})
        if r.ok:
            st.session_state['sec_filings'] = r.json()['filings']
            st.success('Loaded SEC filings!')
        else:
            st.error('Failed to fetch SEC filings.')
else:
    st.sidebar.header('Data')
    if st.sidebar.button('Generate Synthetic Data'):
        response = requests.get(f'{BACKEND_URL}/generate-data')
        if response.ok:
            st.session_state['data'] = response.json()
        else:
            st.error('Failed to generate data.')
    uploaded = st.sidebar.file_uploader('Upload CSV (prices)', type=['csv'])
    if uploaded:
        df = pd.read_csv(uploaded)
        if 'price' in df.columns:
            st.session_state['data'] = st.session_state.get('data', {})
            st.session_state['data']['prices'] = df['price'].tolist()
            st.success('Uploaded price data!')

# --- User Settings ---
st.sidebar.header('Settings')
forecast_method = st.sidebar.selectbox('Forecast Method', ['arima', 'lstm', 'prophet', 'xgboost'])
forecast_steps = st.sidebar.slider('Forecast Steps', 1, 30, 5)
risk_aversion = st.sidebar.slider('Risk Aversion', 0.0, 1.0, 0.5)

# --- Main Pages ---
data = st.session_state.get('data', None)
news = st.session_state.get('news', None)
sec_filings = st.session_state.get('sec_filings', None)

if page == 'Data':
    st.title('💰 Autonomous Financial Analyst')
    st.markdown('''Feed in financial reports, stock data, and market news to get in-depth analysis, risk metrics, and future forecasts. Optionally, optimize your portfolio!''')
    if data:
        st.subheader('Loaded Data')
        st.write('**Assets:**', data.get('assets', []))
        st.write('**Stock Prices:**')
        st.line_chart(pd.Series(data.get('prices', []), name='Price'))
        if 'dates' in data:
            st.write('**Dates:**', data['dates'][:5], '...')
    else:
        st.info('Load data using the sidebar to get started.')
    if news:
        st.subheader('News Headlines')
        for i, n in enumerate(news):
            st.write('-', n['headline'])
            # LLM Summarization for news
            if st.button(f'Summarize News {i+1}', key=f'sum_news_{i}'):
                r = requests.post(f'{BACKEND_URL}/summarize', json={'text': n['headline']})
                if r.ok:
                    st.info('Summary: ' + r.json()['summary'])
                else:
                    st.error('Failed to summarize.')
    else:
        st.info('Load news using the sidebar.')
if page == 'SEC Filings':
    st.header('📄 SEC Filings')
    if sec_filings:
        for i, filing in enumerate(sec_filings):
            st.write(f"[{filing['type']} - {filing['date']}]({filing['url']})")
            # LLM Summarization for SEC filings (URL only, placeholder)
            if st.button(f'Summarize Filing {i+1}', key=f'sum_filing_{i}'):
                r = requests.post(f'{BACKEND_URL}/summarize', json={'text': filing['url']})
                if r.ok:
                    st.info('Summary: ' + r.json()['summary'])
                else:
                    st.error('Failed to summarize.')
    else:
        st.info('Load SEC filings using the sidebar.')

if data:
    if page == 'Analysis':
        st.header('📊 Financial Analysis')
        if st.button('Run Analysis'):
            r = requests.post(f'{BACKEND_URL}/analyze', json=data)
            st.session_state['analysis'] = r.json() if r.ok else None
        if 'analysis' in st.session_state:
            st.json(st.session_state['analysis'])
            analysis_json = json.dumps(st.session_state['analysis'], indent=2)
            st.download_button('Download Analysis (JSON)', data=analysis_json, file_name='analysis.json', mime='application/json')
    if page == 'Forecast':
        st.header('📈 Price Forecast')
        if st.button('Run Forecast'):
            r = requests.post(f'{BACKEND_URL}/forecast?method='+forecast_method+'&steps='+str(forecast_steps), json=data)
            st.session_state['forecast'] = r.json() if r.ok else None
        if 'forecast' in st.session_state:
            forecast = st.session_state['forecast']['forecast']
            actual = data['prices']
            fig = go.Figure()
            fig.add_trace(go.Scatter(y=actual, mode='lines', name='Actual'))
            fig.add_trace(go.Scatter(y=forecast, mode='lines', name='Forecast'))
            st.plotly_chart(fig, use_container_width=True)
            min_len = min(len(actual), len(forecast))
            df_download = pd.DataFrame({'actual': actual[:min_len], 'forecast': forecast[:min_len]})
            csv = df_download.to_csv(index=False)
            st.download_button('Download Forecast (CSV)', data=csv, file_name='forecast.csv', mime='text/csv')
            # XGBoost Explainability
            if forecast_method == 'xgboost':
                if st.button('Explain XGBoost Forecast'):
                    r = requests.post(f'{BACKEND_URL}/explain-forecast', json={'prices': actual, 'steps': forecast_steps, 'window': 5})
                    if r.ok:
                        shap_vals = r.json().get('shap_values', [])
                        eli5_html = r.json().get('eli5_html', '')
                        st.subheader('SHAP Values')
                        st.write(shap_vals)
                        st.subheader('ELI5 Explanation')
                        components.html(eli5_html, height=400, scrolling=True)
                    else:
                        st.error('Failed to explain XGBoost forecast.')
    if page == 'Sentiment':
        st.header('📰 Sentiment Analysis')
        if st.button('Run Sentiment Analysis'):
            r = requests.post(f'{BACKEND_URL}/sentiment', json=data)
            st.session_state['sentiment'] = r.json() if r.ok else None
        if 'sentiment' in st.session_state:
            st.json(st.session_state['sentiment'])
    if page == 'Risk':
        st.header('⚠️ Risk Metrics')
        if st.button('Calculate Risk Metrics'):
            r = requests.post(f'{BACKEND_URL}/risk', json=data)
            st.session_state['risk'] = r.json() if r.ok else None
        if 'risk' in st.session_state:
            st.json(st.session_state['risk'])
    if page == 'Portfolio':
        st.header('💼 Portfolio Optimization')
        if st.button('Optimize Portfolio'):
            r = requests.post(f'{BACKEND_URL}/optimize?risk_aversion='+str(risk_aversion), json=data)
            st.session_state['optimize'] = r.json() if r.ok else None
        if 'optimize' in st.session_state:
            st.json(st.session_state['optimize'])
            portfolio_json = json.dumps(st.session_state['optimize'], indent=2)
            st.download_button('Download Portfolio (JSON)', data=portfolio_json, file_name='portfolio.json', mime='application/json') 
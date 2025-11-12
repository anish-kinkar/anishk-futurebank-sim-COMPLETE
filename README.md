# FutureBank Sim — Streamlit Deployment Pack

AI-driven personal wealth predictor using Monte Carlo simulation.

## Features
- Income, expense, savings, and inflation modeling
- Portfolio return simulation
- Optional purchase (car/home) scenario with loan
- Monte Carlo (5–95% fan chart)
- Interactive UI via Streamlit

## Run Locally
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app_streamlit.py
```

## Deploy on Streamlit Cloud
1. Push to **public GitHub repo**.
2. Go to https://share.streamlit.io → **New app**.
3. App file: `app_streamlit.py`.
4. Click **Deploy**.

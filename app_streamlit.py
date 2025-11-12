# --- Path hygiene to ensure package is importable on all hosts ---
import os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from futurebank.models import UserProfile, PortfolioConfig, SimulationConfig
from futurebank.simulator import run_monte_carlo

st.set_page_config(page_title="FutureBank Sim", page_icon="💸", layout="wide")

st.title("💸 FutureBank Sim — Personal Wealth Predictor")
st.caption("Interactive Monte Carlo simulator for your financial future.")

with st.sidebar:
    st.header("🎛️ Inputs")
    years = st.slider("Years to simulate", 5, 50, 30, 1)
    n_paths = st.slider("Monte Carlo paths", 100, 5000, 1000, 100)

    st.subheader("You")
    starting_net_worth = st.number_input("Starting Net Worth", value=100000.0, step=1000.0)
    annual_income = st.number_input("Annual Income", value=120000.0, step=1000.0)
    income_growth = st.number_input("Income Growth (annual, e.g. 0.05 = 5%)", value=0.05, step=0.01, format="%.2f")
    savings_rate = st.number_input("Savings Rate (fraction of income)", value=0.25, step=0.01, format="%.2f")
    annual_expenses = st.number_input("Annual Expenses (year 1)", value=60000.0, step=1000.0)
    inflation = st.number_input("Inflation (annual)", value=0.04, step=0.01, format="%.2f")

    st.subheader("Portfolio")
    exp_return = st.number_input("Expected Return (annual)", value=0.07, step=0.01, format="%.2f")
    volatility = st.number_input("Volatility (annual std dev)", value=0.15, step=0.01, format="%.2f")

    st.subheader("Purchase Scenario (optional)")
    enable_purchase = st.checkbox("Include purchase event?", value=False)
    purchase_year = st.slider("Purchase Year (0 = this year)", 0, years-1, 2) if enable_purchase else None
    purchase_amount = st.number_input("Purchase Amount", value=30000.0, step=1000.0) if enable_purchase else 0.0
    use_loan = st.checkbox("Finance with loan?", value=True) if enable_purchase else False
    loan_rate = st.number_input("Loan Interest Rate (annual)", value=0.09, step=0.01, format="%.2f") if enable_purchase and use_loan else 0.0
    loan_years = st.slider("Loan Years", 1, 10, 5) if enable_purchase and use_loan else 0

    seed = st.number_input("Random Seed", value=42, step=1)

user = UserProfile(
    starting_net_worth=starting_net_worth,
    annual_income=annual_income,
    income_growth=income_growth,
    savings_rate=savings_rate,
    annual_expenses=annual_expenses,
    inflation=inflation,
)
port = PortfolioConfig(exp_return=exp_return, volatility=volatility)
cfg_base = SimulationConfig(years=years, n_paths=n_paths, purchase_year=None, purchase_amount=0.0, use_loan=False, loan_rate=0.0, loan_years=0)

if enable_purchase:
    cfg_buy = SimulationConfig(
        years=years, n_paths=n_paths,
        purchase_year=purchase_year, purchase_amount=purchase_amount,
        use_loan=use_loan, loan_rate=loan_rate, loan_years=loan_years
    )
else:
    cfg_buy = None

# Run simulations
with st.spinner("Running Monte Carlo..."):
    _, base_summary = run_monte_carlo(user, port, cfg_base, seed=int(seed))
    if cfg_buy:
        _, buy_summary = run_monte_carlo(user, port, cfg_buy, seed=int(seed)+1)
    else:
        buy_summary = None

# Plot fan chart
def fan_chart(summary, label: str):
    years_arr = np.arange(summary["p50"].shape[0])
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(years_arr, summary["p50"], label=f"{label} — Median")
    ax.fill_between(years_arr, summary["p5"], summary["p95"], alpha=0.25, label=f"{label} — 5–95%")
    ax.set_xlabel("Year")
    ax.set_ylabel("Net Worth")
    ax.legend(loc="best")
    st.pyplot(fig)

col1, col2 = st.columns(2)
with col1:
    st.subheader("Base Case")
    fan_chart(base_summary, "Base")
with col2:
    st.subheader("Scenario")
    if buy_summary:
        fan_chart(buy_summary, "Purchase")
    else:
        st.info("Enable a purchase in the sidebar to compare scenarios.")

# Simple insights
def insight(summary_a, summary_b=None):
    a_end = summary_a["p50"][-1]
    txt = f"**Base median net worth at year {years}:** {a_end:,.0f}"
    if summary_b:
        b_end = summary_b["p50"][-1]
        delta = b_end - a_end
        emoji = "🟢" if delta > 0 else "🔴"
        txt += f"<br/>{emoji} **Scenario delta vs Base:** {delta:,.0f}"
    return txt

st.markdown("---")
st.markdown(insight(base_summary, buy_summary), unsafe_allow_html=True)

st.caption("Note: This is an educational simulation with simplified assumptions, not financial advice.")

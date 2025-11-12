import numpy as np
from dataclasses import asdict
from .models import UserProfile, PortfolioConfig, SimulationConfig

def amortization_payment(principal: float, rate: float, years: int) -> float:
    if years <= 0:
        return principal
    if rate == 0:
        return principal / years
    r = rate
    n = years
    return principal * (r * (1 + r)**n) / ((1 + r)**n - 1)

def simulate_once(user: UserProfile, port: PortfolioConfig, cfg: SimulationConfig, rng: np.random.Generator):
    years = cfg.years
    net_worth = np.zeros(years + 1)
    portfolio_returns = rng.normal(loc=port.exp_return, scale=port.volatility, size=years)

    nw = user.starting_net_worth
    income = user.annual_income
    expenses = user.annual_expenses

    for t in range(years):
        if t > 0:
            income *= 1 + user.income_growth
            expenses *= 1 + user.inflation

        saved = income * user.savings_rate
        cash_flow = income - expenses
        nw = max(0, nw + cash_flow + saved)
        nw *= (1 + portfolio_returns[t])
        net_worth[t + 1] = nw

    return net_worth

def run_monte_carlo(user: UserProfile, port: PortfolioConfig, cfg: SimulationConfig, seed: int = 42):
    rng = np.random.default_rng(seed)
    paths = np.zeros((cfg.n_paths, cfg.years + 1))
    for i in range(cfg.n_paths):
        paths[i] = simulate_once(user, port, cfg, rng)
    summary = {
        "p5": np.percentile(paths, 5, axis=0),
        "p50": np.percentile(paths, 50, axis=0),
        "p95": np.percentile(paths, 95, axis=0)
    }
    return paths, summary

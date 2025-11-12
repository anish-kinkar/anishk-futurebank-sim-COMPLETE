from dataclasses import dataclass
from typing import Optional

@dataclass
class UserProfile:
    starting_net_worth: float = 100000.0
    annual_income: float = 120000.0
    income_growth: float = 0.05
    savings_rate: float = 0.25
    annual_expenses: float = 60000.0
    inflation: float = 0.04

@dataclass
class PortfolioConfig:
    exp_return: float = 0.07
    volatility: float = 0.15

@dataclass
class SimulationConfig:
    years: int = 30
    n_paths: int = 1000
    purchase_year: Optional[int] = None
    purchase_amount: float = 0.0
    use_loan: bool = False
    loan_rate: float = 0.09
    loan_years: int = 5

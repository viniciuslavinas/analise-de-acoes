from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Company:
    ticker: str
    name: str
    sector: str
    price: float
    shares_millions: float
    revenue_millions: float
    ebit_margin: float
    tax_rate: float
    depreciation_millions: float
    capex_millions: float
    working_capital_change_millions: float
    net_debt_millions: float
    book_value_millions: float
    net_income_millions: float
    dividends_per_share: float
    revenue_growth: float
    terminal_growth: float
    wacc: float
    cost_of_equity: float
    peer_pe: float
    peer_pb: float
    peer_ev_ebitda: float
    peer_ev_ebit: float
    peer_peg: float


@dataclass(frozen=True)
class Assumptions:
    revenue_growth: float
    ebit_margin: float
    wacc: float
    terminal_growth: float
    payout_growth: float


def update_company(company: Company, **values: float) -> Company:
    return replace(company, **values)

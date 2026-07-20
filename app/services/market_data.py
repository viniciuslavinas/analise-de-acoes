from app.data.repository import list_companies, set_price
from app.domain import Company


def refresh_prices() -> list[str]:
    """Atualiza cotações. O sufixo .SA é usado para ativos da B3 no Yahoo Finance."""
    import yfinance as yf
    updated = []
    for company in list_companies():
        history = yf.Ticker(f"{company.ticker}.SA").history(period="5d")
        if not history.empty:
            set_price(company.ticker, round(float(history["Close"].iloc[-1]), 2))
            updated.append(company.ticker)
    return updated


SECTOR_MULTIPLES = {
    "Financial Services": (9.0, 1.4, 6.0, 12.0, 1.0),
    "Utilities": (10.0, 1.5, 6.0, 11.0, 1.0),
    "Energy": (7.0, 1.3, 4.5, 8.0, .9),
    "Basic Materials": (8.0, 1.6, 5.5, 9.0, 1.0),
    "Consumer Defensive": (16.0, 3.0, 9.0, 14.0, 1.4),
    "Industrials": (15.0, 3.0, 9.0, 14.0, 1.3),
    "Technology": (22.0, 5.0, 14.0, 20.0, 1.7),
}


def _latest(frame, row: str, fallback: float = 0) -> float:
    """Lê a coluna mais recente de uma demonstração do yfinance."""
    try:
        value = frame.loc[row].dropna().iloc[0]
        return float(value)
    except (KeyError, IndexError, AttributeError, TypeError, ValueError):
        return fallback


def company_from_ticker(ticker: str) -> Company:
    """Cria um cadastro inicial usando dados públicos do Yahoo Finance."""
    import yfinance as yf

    symbol = f"{ticker.upper().replace('.SA', '')}.SA"
    asset = yf.Ticker(symbol)
    info = asset.info
    price = float(info.get("regularMarketPrice") or info.get("currentPrice") or 0)
    shares = float(info.get("sharesOutstanding") or 0) / 1_000_000
    income, balance, cashflow = asset.financials, asset.balance_sheet, asset.cashflow
    revenue = _latest(income, "Total Revenue") / 1_000_000
    ebit = _latest(income, "EBIT") / 1_000_000
    ebitda = _latest(income, "EBITDA") / 1_000_000
    net_income = _latest(income, "Net Income") / 1_000_000
    total_debt = _latest(balance, "Total Debt") / 1_000_000
    cash = _latest(balance, "Cash Cash Equivalents And Short Term Investments") / 1_000_000
    equity = _latest(balance, "Stockholders Equity") / 1_000_000
    capex = abs(_latest(cashflow, "Capital Expenditure")) / 1_000_000
    change_wc = _latest(cashflow, "Change In Working Capital") / 1_000_000
    sector = info.get("sector") or "Outros"
    if not price or not shares or not revenue:
        raise ValueError("Não foram encontrados dados suficientes para este ticker na B3.")
    peers = SECTOR_MULTIPLES.get(sector, (12.0, 2.0, 8.0, 12.0, 1.2))
    return Company(
        ticker.upper().replace(".SA", ""), info.get("longName") or ticker.upper(), sector,
        price, shares, revenue, ebit / revenue if revenue else .1, .34,
        max(ebitda - ebit, 0), capex, change_wc, total_debt - cash, equity or revenue * .4,
        net_income, float(info.get("trailingAnnualDividendRate") or 0),
        float(info.get("revenueGrowth") or .05), .04, .12, .15, *peers,
    )

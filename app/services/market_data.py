from app.data.repository import list_companies, set_price


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

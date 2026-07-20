import json
from pathlib import Path
from app.domain import Company


# Demonstração: valores em R$ milhões, salvo preço e dividendos por ação.
COMPANIES = [
    Company("ITUB4", "Itaú Unibanco PN", "Financeiro", 36.42, 9_900, 205_000, .34, .30, 4_100, 5_900, 1_100, -22_000, 197_000, 41_500, 1.55, .09, .045, .115, .14, 9.0, 1.55, 6.0, 14.5, 1.1),
    Company("WEGE3", "WEG ON", "Bens de capital", 51.88, 4_200, 38_100, .22, .34, 760, 1_050, 560, -2_100, 8_800, 6_100, .36, .13, .05, .105, .12, 24.0, 6.2, 16.0, 28.0, 1.8),
    Company("TAEE11", "Taesa Units", "Energia elétrica", 36.75, 1_100, 4_200, .61, .34, 490, 630, 170, 8_400, 7_100, 1_900, 3.10, .06, .045, .105, .11, 10.0, 1.4, 5.8, 10.5, 1.0),
    Company("BBAS3", "Banco do Brasil ON", "Financeiro", 28.94, 2_850, 240_000, .31, .30, 3_600, 4_500, 1_300, -12_000, 160_000, 37_000, 1.78, .08, .045, .12, .15, 8.5, 1.3, 5.5, 12.0, 1.0),
]
PRICE_FILE = Path(__file__).with_name("prices.json")
COMPANY_FILE = Path(__file__).with_name("companies.json")
REMOVED_FILE = Path(__file__).with_name("removed.json")


def _load_price_overrides() -> None:
    if not PRICE_FILE.exists():
        return
    try:
        overrides = json.loads(PRICE_FILE.read_text())
    except json.JSONDecodeError:
        return
    for ticker, price in overrides.items():
        set_price(ticker, float(price), save=False)


def list_companies() -> list[Company]:
    return COMPANIES


def get_company(ticker: str) -> Company | None:
    return next((item for item in COMPANIES if item.ticker == ticker.upper()), None)


def add_company(company: Company) -> Company:
    if get_company(company.ticker):
        raise ValueError("Este ticker já está cadastrado.")
    COMPANIES.append(company)
    custom = json.loads(COMPANY_FILE.read_text()) if COMPANY_FILE.exists() else []
    custom.append(company.__dict__)
    COMPANY_FILE.write_text(json.dumps(custom, indent=2, ensure_ascii=False) + "\n")
    set_price(company.ticker, company.price)
    return company


def remove_company(ticker: str) -> bool:
    ticker = ticker.upper()
    index = next((i for i, item in enumerate(COMPANIES) if item.ticker == ticker), None)
    if index is None:
        return False
    COMPANIES.pop(index)
    removed = json.loads(REMOVED_FILE.read_text()) if REMOVED_FILE.exists() else []
    if ticker not in removed:
        removed.append(ticker)
        REMOVED_FILE.write_text(json.dumps(removed, indent=2) + "\n")
    if COMPANY_FILE.exists():
        custom = [item for item in json.loads(COMPANY_FILE.read_text()) if item["ticker"] != ticker]
        COMPANY_FILE.write_text(json.dumps(custom, indent=2, ensure_ascii=False) + "\n")
    return True


def set_price(ticker: str, price: float, save: bool = True) -> bool:
    for index, company in enumerate(COMPANIES):
        if company.ticker == ticker.upper():
            COMPANIES[index] = Company(**{**company.__dict__, "price": price})
            if save:
                PRICE_FILE.write_text(json.dumps({item.ticker: item.price for item in COMPANIES}, indent=2) + "\n")
            return True
    return False


_load_price_overrides()


def _load_custom_companies() -> None:
    if not COMPANY_FILE.exists():
        return
    try:
        for values in json.loads(COMPANY_FILE.read_text()):
            if not get_company(values["ticker"]):
                COMPANIES.append(Company(**values))
    except (json.JSONDecodeError, KeyError, TypeError):
        return


_load_custom_companies()


def _load_removed_companies() -> None:
    if not REMOVED_FILE.exists():
        return
    try:
        removed = set(json.loads(REMOVED_FILE.read_text()))
        COMPANIES[:] = [item for item in COMPANIES if item.ticker not in removed]
    except json.JSONDecodeError:
        return


_load_removed_companies()

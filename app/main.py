from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from app.data.repository import add_company, get_company, list_companies
from app.domain import Assumptions, Company
from app.services.market_data import company_from_ticker
from app.services.valuation import analysis

ROOT = Path(__file__).parent
app = FastAPI(title="Análise de Ações", version="0.1.0")
app.mount("/static", StaticFiles(directory=ROOT / "static"), name="static")
templates = Jinja2Templates(directory=ROOT / "templates")


class SimulationInput(BaseModel):
    revenue_growth: float = Field(ge=-0.5, le=1)
    ebit_margin: float = Field(ge=-1, le=1)
    wacc: float = Field(gt=0, le=1)
    terminal_growth: float = Field(ge=-0.2, le=.2)
    payout_growth: float = Field(ge=-0.2, le=.2)


class CompanyInput(BaseModel):
    ticker: str = Field(min_length=4, max_length=8)
    name: str = Field(min_length=2, max_length=80)
    sector: str = Field(min_length=2, max_length=60)
    price: float = Field(gt=0)
    shares_millions: float = Field(gt=0)
    revenue_millions: float = Field(gt=0)
    ebit_margin: float = Field(ge=-1, le=1)
    tax_rate: float = Field(ge=0, le=1)
    depreciation_millions: float = Field(ge=0)
    capex_millions: float = Field(ge=0)
    working_capital_change_millions: float
    net_debt_millions: float
    book_value_millions: float = Field(gt=0)
    net_income_millions: float
    dividends_per_share: float = Field(ge=0)
    revenue_growth: float = Field(ge=-.5, le=1)
    terminal_growth: float = Field(ge=-.1, le=.2)
    wacc: float = Field(gt=0, le=1)
    cost_of_equity: float = Field(gt=0, le=1)
    peer_pe: float = Field(gt=0)
    peer_pb: float = Field(gt=0)
    peer_ev_ebitda: float = Field(gt=0)
    peer_ev_ebit: float = Field(gt=0)
    peer_peg: float = Field(gt=0)


def public(result: dict) -> dict:
    company = result["company"]
    return {"ticker": company.ticker, "name": company.name, "sector": company.sector, "price": company.price, "reference_value": result["reference_value"], "safety_margin": result["safety_margin"], "quality": result["quality"], "dcf": result["dcf"], "ddm": result["ddm"], "multiples": result["multiples"]}


@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    items = [public(analysis(company)) for company in list_companies()]
    return templates.TemplateResponse(request, "dashboard.html", {"items": items})


@app.get("/acoes/{ticker}", response_class=HTMLResponse)
def company_page(request: Request, ticker: str):
    company = get_company(ticker)
    if not company:
        raise HTTPException(404, "Ação não encontrada")
    return templates.TemplateResponse(request, "company.html", {"item": public(analysis(company))})


@app.get("/api/acoes")
def api_companies():
    return [public(analysis(company)) for company in list_companies()]


@app.get("/api/acoes/{ticker}")
def api_company(ticker: str):
    company = get_company(ticker)
    if not company:
        raise HTTPException(404, "Ação não encontrada")
    return public(analysis(company))


@app.post("/api/acoes/{ticker}/simular")
def simulate(ticker: str, values: SimulationInput):
    company = get_company(ticker)
    if not company:
        raise HTTPException(404, "Ação não encontrada")
    try:
        return public(analysis(company, Assumptions(**values.model_dump())))
    except ValueError as error:
        raise HTTPException(422, str(error))


@app.post("/api/acoes", status_code=201)
def create_company(values: CompanyInput):
    try:
        company = add_company(Company(**{**values.model_dump(), "ticker": values.ticker.upper()}))
        return public(analysis(company))
    except ValueError as error:
        raise HTTPException(422, str(error))


@app.post("/api/acoes/importar/{ticker}", status_code=201)
def import_company(ticker: str):
    try:
        company = add_company(company_from_ticker(ticker))
        return public(analysis(company))
    except ValueError as error:
        raise HTTPException(422, str(error))
    except Exception:
        raise HTTPException(503, "Não foi possível consultar a fonte de dados agora. Tente novamente em instantes.")

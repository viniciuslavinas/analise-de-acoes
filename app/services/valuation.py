from dataclasses import asdict
from app.domain import Assumptions, Company


def default_assumptions(company: Company) -> Assumptions:
    return Assumptions(company.revenue_growth, company.ebit_margin, company.wacc, company.terminal_growth, company.revenue_growth)


def dcf(company: Company, assumptions: Assumptions | None = None, years: int = 5) -> dict:
    a = assumptions or default_assumptions(company)
    if a.wacc <= a.terminal_growth:
        raise ValueError("O WACC deve ser maior que o crescimento terminal.")
    revenue = company.revenue_millions
    present_value = 0.0
    projections = []
    for year in range(1, years + 1):
        revenue *= 1 + a.revenue_growth
        nopat = revenue * a.ebit_margin * (1 - company.tax_rate)
        fcf = nopat + company.depreciation_millions - company.capex_millions - company.working_capital_change_millions
        pv = fcf / (1 + a.wacc) ** year
        present_value += pv
        projections.append({"year": year, "revenue": revenue, "fcf": fcf, "pv": pv})
    terminal_value = projections[-1]["fcf"] * (1 + a.terminal_growth) / (a.wacc - a.terminal_growth)
    enterprise_value = present_value + terminal_value / (1 + a.wacc) ** years
    equity_value = enterprise_value - company.net_debt_millions
    per_share = equity_value / company.shares_millions
    return {"per_share": per_share, "enterprise_value": enterprise_value, "equity_value": equity_value, "projections": projections, "assumptions": asdict(a)}


def ddm(company: Company, dividend_growth: float | None = None) -> dict:
    growth = dividend_growth if dividend_growth is not None else company.terminal_growth
    if company.cost_of_equity <= growth:
        return {"per_share": None, "warning": "O custo de capital próprio deve superar o crescimento perpétuo."}
    return {"per_share": company.dividends_per_share * (1 + growth) / (company.cost_of_equity - growth), "growth": growth}


def multiples(company: Company) -> dict:
    eps = company.net_income_millions / company.shares_millions
    bvps = company.book_value_millions / company.shares_millions
    ebit = company.revenue_millions * company.ebit_margin
    ebitda = ebit + company.depreciation_millions
    ev = company.price * company.shares_millions + company.net_debt_millions
    growth_percent = max(company.revenue_growth * 100, .1)
    current = {"pe": company.price / eps, "pb": company.price / bvps, "ev_ebitda": ev / ebitda, "ev_ebit": ev / ebit, "peg": (company.price / eps) / growth_percent}
    implied = {"pe": eps * company.peer_pe, "pb": bvps * company.peer_pb, "ev_ebitda": (company.peer_ev_ebitda * ebitda - company.net_debt_millions) / company.shares_millions, "ev_ebit": (company.peer_ev_ebit * ebit - company.net_debt_millions) / company.shares_millions, "peg": eps * company.peer_peg * growth_percent}
    return {"current": current, "implied": implied, "per_share": sum(implied.values()) / len(implied)}


def quality_metrics(company: Company) -> dict:
    ebit = company.revenue_millions * company.ebit_margin
    invested_capital = company.book_value_millions + company.net_debt_millions
    fcf = ebit * (1 - company.tax_rate) + company.depreciation_millions - company.capex_millions - company.working_capital_change_millions
    return {"roe": company.net_income_millions / company.book_value_millions, "roic": ebit * (1 - company.tax_rate) / invested_capital, "ebit_margin": company.ebit_margin, "net_margin": company.net_income_millions / company.revenue_millions, "net_debt_ebitda": company.net_debt_millions / (ebit + company.depreciation_millions), "fcf_millions": fcf}


def analysis(company: Company, assumptions: Assumptions | None = None) -> dict:
    dcf_result = dcf(company, assumptions)
    ddm_result = ddm(company, assumptions.payout_growth if assumptions else None)
    multiple_result = multiples(company)
    values = [dcf_result["per_share"], multiple_result["per_share"]]
    if ddm_result["per_share"]:
        values.append(ddm_result["per_share"])
    average = sum(values) / len(values)
    return {"company": company, "dcf": dcf_result, "ddm": ddm_result, "multiples": multiple_result, "quality": quality_metrics(company), "reference_value": average, "safety_margin": (average / company.price) - 1}

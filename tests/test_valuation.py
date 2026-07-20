from app.data.repository import get_company
from app.services.valuation import analysis, dcf, multiples


def test_dcf_returns_positive_value():
    result = dcf(get_company("WEGE3"))
    assert result["per_share"] > 0
    assert len(result["projections"]) == 5


def test_analysis_exposes_all_methods():
    result = analysis(get_company("TAEE11"))
    assert result["reference_value"] > 0
    assert set(multiples(get_company("TAEE11"))["current"]) == {"pe", "pb", "ev_ebitda", "ev_ebit", "peg"}

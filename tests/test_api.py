import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_health(client):
    rv = client.get("/api/v1/health")
    assert rv.status_code == 200
    assert rv.json["status"] == "ok"


def test_alloc_income(client):
    rv = client.post(
        "/api/v1/calculate/alloc-income",
        json={"income": 5000000, "allocation_type": "saving", "percentage": 20},
    )
    assert rv.status_code == 200
    assert rv.json["amount"] == 1000000.0
    assert rv.json["allocation_label"] == "Menabung/Investasi"


def test_alloc_income_invalid(client):
    rv = client.post(
        "/api/v1/calculate/alloc-income",
        json={"income": -1, "allocation_type": "saving", "percentage": 20},
    )
    assert rv.status_code == 400


def test_bep(client):
    rv = client.post(
        "/api/v1/calculate/bep",
        json={"fixed_costs": 100000, "variable_costs": 25000, "selling_price": 50000},
    )
    assert rv.status_code == 200
    assert rv.json["bep_units"] == 4.0


def test_financial(client):
    rv = client.post(
        "/api/v1/calculate/financial",
        json={"income": 10000000, "expenses": 7000000},
    )
    assert rv.status_code == 200
    assert rv.json["profit"] == 3000000.0
    assert rv.json["is_profit"] is True


def test_investment(client):
    rv = client.post(
        "/api/v1/calculate/investment",
        json={"initial": 10000000, "rate": 10, "years": 5},
    )
    assert rv.status_code == 200
    assert rv.json["years"] == 5
    assert len(rv.json["growth_series"]) == 6


def test_profit_loss(client):
    rv = client.post(
        "/api/v1/calculate/profit-loss",
        json={"revenue": 100000, "expenses": 80000},
    )
    assert rv.status_code == 200
    assert rv.json["status_label"] == "Laba"


def test_tax(client):
    rv = client.post(
        "/api/v1/calculate/tax",
        json={"revenue": 200000, "expenses": 50000},
    )
    assert rv.status_code == 200
    assert rv.json["tax"] == 15000.0


def test_evaluate_safe(client):
    rv = client.post(
        "/api/v1/calculate/evaluate",
        json={"expression": "2+3*4"},
    )
    assert rv.status_code == 200
    assert rv.json["result"] == 14.0


def test_evaluate_injection(client):
    rv = client.post(
        "/api/v1/calculate/evaluate",
        json={"expression": "__import__('os').system('ls')"},
    )
    assert rv.status_code == 400
    assert rv.json["status"] == "error"


def test_404(client):
    rv = client.get("/nonexistent")
    assert rv.status_code == 404


def test_invalid_json(client):
    rv = client.post(
        "/api/v1/calculate/alloc-income",
        data="not-json",
        content_type="application/json",
    )
    assert rv.status_code == 400

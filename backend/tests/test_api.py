"""
API integration tests using FastAPI TestClient.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import init_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    init_db()


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["model_loaded"] is True
    assert "version" in data


def test_dashboard_summary():
    response = client.get("/api/dashboard/summary")
    assert response.status_code == 200
    data = response.json()
    assert "stat_cards" in data
    assert len(data["stat_cards"]) == 4
    assert "trend_data" in data
    assert len(data["trend_data"]) > 0
    assert "risk_distribution" in data
    assert "latest_reading" in data


def test_create_prediction():
    payload = {
        "PT08.S1(CO)": 1360.0,
        "PT08.S2(NMHC)": 1046.0,
        "PT08.S3(NOx)": 1056.0,
        "PT08.S4(NO2)": 1692.0,
        "PT08.S5(O3)": 1268.0,
        "T": 13.6,
        "RH": 48.9,
        "AH": 0.7578,
        "Hour": 18,
        "DayOfWeek": 2
    }
    response = client.post("/api/predictions", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "predicted_concentration" in data
    assert data["predicted_concentration"] > 0
    assert "risk_category" in data
    assert data["unit"] == "µg/m³"
    assert "id" in data


def test_get_history():
    response = client.get("/api/history?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert "predicted_concentration" in data[0]
        assert "risk_category" in data[0]


def test_get_historical_data():
    response = client.get("/api/historical-data?page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert data["total_records"] == 9357
    assert data["page"] == 1
    assert data["page_size"] == 10
    assert len(data["records"]) == 10


def test_get_model_info():
    response = client.get("/api/model-info")
    assert response.status_code == 200
    data = response.json()
    assert "model_name" in data
    assert "evaluation" in data
    assert "test_r2" in data["evaluation"]
    assert "actual_vs_predicted_sample" in data

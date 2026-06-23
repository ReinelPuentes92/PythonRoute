import pytest
from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_get_time_returns_all_countries():
    """Test that /time endpoint returns data for all three countries."""
    response = client.get("/time")
    assert response.status_code == 200

    data = response.json()
    assert "colombia" in data
    assert "ecuador" in data
    assert "peru" in data


def test_get_time_structure():
    """Test that each country has required fields."""
    response = client.get("/time")
    data = response.json()

    for country in ["colombia", "ecuador", "peru"]:
        country_data = data[country]
        assert "timezone" in country_data
        assert "time" in country_data
        assert "hour" in country_data
        assert "minute" in country_data

        # Validate types
        assert isinstance(country_data["timezone"], str)
        assert isinstance(country_data["time"], str)
        assert isinstance(country_data["hour"], int)
        assert isinstance(country_data["minute"], int)

        # Validate hour and minute ranges
        assert 0 <= country_data["hour"] < 24
        assert 0 <= country_data["minute"] < 60


def test_get_time_timezones():
    """Test that correct timezones are returned."""
    response = client.get("/time")
    data = response.json()

    assert data["colombia"]["timezone"] == "America/Bogota"
    assert data["ecuador"]["timezone"] == "America/Guayaquil"
    assert data["peru"]["timezone"] == "America/Lima"


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

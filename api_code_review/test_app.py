from fastapi.testclient import TestClient

from api_code_review.app import app

client = TestClient(app)

VALID_DAYS = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"}


def test_get_day_returns_all_countries():
    """Test that /day endpoint returns data for all three countries."""
    response = client.get("/day")
    assert response.status_code == 200

    data = response.json()
    assert "colombia" in data
    assert "china" in data
    assert "espana" in data


def test_get_day_structure():
    """Test that each country has required fields with correct types."""
    response = client.get("/day")
    data = response.json()

    for country in ["colombia", "china", "espana"]:
        country_data = data[country]
        assert "timezone" in country_data
        assert "day_of_week" in country_data
        assert "day_number" in country_data
        assert "date" in country_data

        assert isinstance(country_data["timezone"], str)
        assert isinstance(country_data["day_of_week"], str)
        assert isinstance(country_data["day_number"], int)
        assert isinstance(country_data["date"], str)


def test_get_day_valid_values():
    """Test that day values are within valid ranges."""
    response = client.get("/day")
    data = response.json()

    for country in ["colombia", "china", "espana"]:
        country_data = data[country]
        assert country_data["day_of_week"] in VALID_DAYS
        assert 0 <= country_data["day_number"] <= 6


def test_get_day_timezones():
    """Test that correct timezones are returned for each country."""
    response = client.get("/day")
    data = response.json()

    assert data["colombia"]["timezone"] == "America/Bogota"
    assert data["china"]["timezone"] == "Asia/Shanghai"
    assert data["espana"]["timezone"] == "Europe/Madrid"


def test_get_day_date_format():
    """Test that date follows YYYY-MM-DD format."""
    import re

    response = client.get("/day")
    data = response.json()

    date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    for country in ["colombia", "china", "espana"]:
        assert date_pattern.match(data[country]["date"]), (
            f"Date format invalid for {country}: {data[country]['date']}"
        )


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

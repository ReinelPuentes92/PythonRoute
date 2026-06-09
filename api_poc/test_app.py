from fastapi.testclient import TestClient

from api_poc.app import app

client = TestClient(app)


def test_get_hour_returns_time_payload() -> None:
    response = client.get("/hour")

    assert response.status_code == 200

    data = response.json()
    assert set(data.keys()) == {"hour", "minute", "second", "iso_utc"}

    assert isinstance(data["hour"], int)
    assert 0 <= data["hour"] <= 23

    assert isinstance(data["minute"], int)
    assert 0 <= data["minute"] <= 59

    assert isinstance(data["second"], int)
    assert 0 <= data["second"] <= 59

    assert isinstance(data["iso_utc"], str)
    assert "T" in data["iso_utc"]

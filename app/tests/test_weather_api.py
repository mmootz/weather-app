from backend.weather_api import app
from unittest.mock import patch
import requests


@patch("backend.weather_api.requests.get")
def test_weather_timeout(mock_get):
    mock_get.side_effect = requests.exceptions.Timeout  # Simulate timeout

    with app.test_client() as client:
        resp = client.get("/weather?city=somewhere")

    assert resp.status_code == 504
    data = resp.get_json()
    assert "timed out" in data["error"].lower()

@patch("backend.weather_api.requests.get")
def test_weather_api_failure(mock_get):
    mock_get.side_effect = requests.exceptions.RequestException("Network error")

    with app.test_client() as client:
        resp = client.get("/weather?city=nowhere")

    assert resp.status_code == 502
    data = resp.get_json()
    assert "failed to fetch" in data["error"].lower()

def test_healthz():
    with app.test_client() as client:
        resp = client.get("/healthz")

    assert resp.status_code == 200
    data = resp.get_json()
    assert data["status"] == "Healthy"

@patch("backend.weather_api.redis_client")
def test_ready_ok(mock_redis):
    mock_redis.ping.return_value = True

    with app.test_client() as client:
        resp = client.get("/ready")

    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ready"

@patch("backend.weather_api.redis_client")
def test_ready_redis_down(mock_redis):
    import redis
    mock_redis.ping.side_effect = redis.exceptions.ConnectionError("Cannot connect")

    with app.test_client() as client:
        resp = client.get("/ready")

    assert resp.status_code == 503
    data = resp.get_json()
    assert data["status"] == "not ready"
    assert "redis connection failed" in data["reason"].lower()




    
    

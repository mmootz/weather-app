"""
Tests for
timeout
network error
healthz
ready
200 ok
"""


from unittest.mock import patch, Mock
from backend.weather_api import app, api_call
import redis
import requests


@patch("backend.weather_api.redis_client")
@patch("backend.weather_api.requests.get")
def test_weather_timeout(mock_get, mock_redis):
    """
    Simulate timeout
    """
    mock_get.side_effect = requests.exceptions.Timeout
    mock_redis.get.return_value = None  # Pretend cache is empty
    mock_redis.setex.return_value = True
    with app.test_client() as client:
        resp = client.get("/weather?city=somewhere")

    assert resp.status_code == 504
    data = resp.get_json()
    assert "timed out" in data["error"].lower()

@patch("backend.weather_api.redis_client")
@patch("backend.weather_api.requests.get")
def test_weather_api_failure(mock_get, mock_redis):
    """
    Simulate network error
    """
    mock_get.side_effect = requests.exceptions.RequestException("Network error")
    mock_redis.get.return_value = None
    with app.test_client() as client:
        resp = client.get("/weather?city=nowhere")

    assert resp.status_code == 502
    data = resp.get_json()
    assert "failed to fetch" in data["error"].lower()

def test_healthz():
    """
    test healthz for health probe
    """
    with app.test_client() as client:
        resp = client.get("/healthz")

    assert resp.status_code == 200
    data = resp.get_json()
    assert data["status"] == "Healthy"

@patch("backend.weather_api.redis_client")
def test_ready_ok(mock_redis):
    """
    200 ok
    """
    mock_redis.ping.return_value = True

    with app.test_client() as client:
        resp = client.get("/ready")

    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ready"

@patch("backend.weather_api.redis_client")
def test_ready_redis_down(mock_redis):
    """
    Test connection to redis
    """
    mock_redis.ping.side_effect = redis.exceptions.ConnectionError("Cannot connect")

    with app.test_client() as client:
        resp = client.get("/ready")

    assert resp.status_code == 503
    data = resp.get_json()
    assert data["status"] == "not ready"
    assert "redis connection failed" in data["reason"].lower()
@patch("backed.weather_api.api_call")
def test_api_call_success():
    """
    Docstring for test_api_call
    :param mock_redis: Description
    """
    
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"ok" : True}

    with patch("weather_api.requests.get", return_value=mock_response):
        result = api_call("http://example.com")

    assert result == {"ok" : True }
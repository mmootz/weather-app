from backend.weather_api import app, weather
from flask import Flask
import pytest
import requests
from unittest.mock import patch, MagicMock

app = Flask(__name__)

@patch("backend.weather_api.requests.get")
def test_weather_returns_200(mock_get):
    # Create a fake response object
    mock_response = MagicMock()
    mock_response.json.return_value = {"temp": 70, "city": "La Mirada"}
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    with app.test_request_context("/weather?city=somewhere"):
        response = weather()
    
    # Assert that the function did what we expect
   # mock_get.assert_called_once()
    assert response.status_code == 200

@patch("backend.weather_api.requests.get")
def test_weather_timeout(mock_get):
    mock_get.side_effect = requests.exceptions.Timeout

    with app.test_client() as client:
        resp = client.get("/weather?city=somewhere")
        
    assert resp.status_code == 504
    assert "timed out" in resp.get_json()["error"].lower()

    
    

# test_api.py
import pytest

# Assume `get_weather_data` is implemented to handle different responses
def get_weather_data(location):
    import requests
    try:
        response = requests.get(
            f"http://api.weather.com/data?location={location}"
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise e

def test_weather_success_valid_data(mock_weather_response_factory):
    """Test successful API call returns expected data."""
    mock_weather_response_factory(status_code=200, json_data={"temperature": 22})
    result = get_weather_data("London")
    assert result["temperature"] == 22
    assert "temperature" in result

def test_weather_success_with_different_data(mock_weather_response_factory):
    """Test successful API call with different data."""
    mock_weather_response_factory(status_code=200, json_data={"temperature": 15})
    result = get_weather_data("Berlin")
    assert result["temperature"] == 15

def test_weather_success_malformed_data(mock_weather_response_factory):
    """Test for malformed data from a successful API call."""
    mock_weather_response_factory(status_code=200, json_data={"temp": 22})
    
    # This test will likely fail with a KeyError, which is the point
    # We are testing that our function can gracefully handle this unexpected data
    with pytest.raises(KeyError):
        get_weather_data("Unknown")

def test_weather_failure_status_code(mock_weather_response_factory):
    """Test the function correctly handles a 404 response."""
    mock_weather_response_factory(status_code=404, json_data={})
    with pytest.raises(requests.exceptions.HTTPError):
        get_weather_data("Invalid City")


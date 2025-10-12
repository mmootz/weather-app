
# conftest.py
import pytest
import requests

@pytest.fixture
def weather_api_success_factory(monkeypatch):
    """
    Returns a factory function to create a mock for a successful API call.
    """
    def make_mock_response(temperature):
        """Creates a mock response with a specified temperature."""
        class MockResponse:
            def raise_for_status(self):
                pass
            def json(self):
                return {"temperature": temperature}
        
        def mock_get(*args, **kwargs):
            return MockResponse()

        monkeypatch.setattr("backend.weather_api.weather", mock_get)
    
    return make_mock_response

@pytest.fixture
def mock_weather_timeout(monkeypatch):
    """Mocks a requests.exceptions.Timeout error during an API call."""
    def mock_get(*args, **kwargs):
        raise requests.exceptions.Timeout("API request timed out")
    monkeypatch.setattr("backend.weather_api.weather.get", mock_get)

    
    
    


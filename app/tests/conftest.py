"""
This isn't used yet

"""

# conftest.py
import os
import pytest

from backend.weather_api import weather

@pytest.fixture(scope='module')
def test_weather_api():
    """
    currently not used
    """
    # Set the Testing configuration prior to creating the Flask application
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    flask_app = weather()

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!

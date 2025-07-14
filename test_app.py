# test_app.py
import pytest
from app import app # Import the Flask app instance from app.py

@pytest.fixture
def client():
    # Configure the Flask app for testing
    app.config['TESTING'] = True
    # Create a test client to make requests to the app
    with app.test_client() as client:
        yield client # Provide the test client to the tests

def test_hello_world(client):
    """
    Test the root ('/') endpoint to ensure it returns the expected greeting.
    """
    rv = client.get('/') # Make a GET request to the root URL
    # Assert that the response data contains the expected byte string
    assert b'Hello, Flask in Docker!' in rv.data

def test_status_endpoint(client):
    """
    Test the '/status' endpoint to ensure it returns 'OK'.
    """
    rv = client.get('/status') # Make a GET request to the /status URL
    # Assert that the response data contains the expected byte string
    assert b'OK' in rv.data

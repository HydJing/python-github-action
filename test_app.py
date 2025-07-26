# test_app.py
import pytest
import json
import os # Import os to manage environment variables for testing
from app import app # Import the Flask app instance from app.py

# --- Pytest Fixture for Test Client Setup ---
@pytest.fixture
def client():
    """
    Configures the Flask application for testing and provides a test client.
    Ensures the app runs in a controlled 'testing' environment.
    """
    # Create a copy of original environment variables to restore later
    original_flask_env = os.environ.get('FLASK_ENV')
    original_app_version = os.environ.get('APP_VERSION')

    # Set environment variables specifically for testing
    os.environ['FLASK_ENV'] = 'testing'
    os.environ['APP_VERSION'] = 'test-version-1.0.0' # Mock a version for testing

    # Configure the Flask app for testing
    # TESTING = True disables error catching during request handling,
    # so errors propagate to the test client.
    app.config['TESTING'] = True
    # Provide a dummy secret key for testing purposes, if your app uses it.
    app.config['SECRET_KEY'] = 'test_secret_key'
    # Ensure debug mode is off for testing, mimicking production behavior where possible.
    app.config['DEBUG'] = False

    # Create a test client to make requests to the app
    # The 'with' statement ensures the client is properly closed after tests.
    with app.test_client() as client:
        yield client # Yield the test client to the tests

    # --- Teardown: Clean up after tests ---
    # Restore original environment variables to avoid side effects on other tests
    if original_flask_env is not None:
        os.environ['FLASK_ENV'] = original_flask_env
    else:
        del os.environ['FLASK_ENV'] # Remove if it wasn't set originally

    if original_app_version is not None:
        os.environ['APP_VERSION'] = original_app_version
    else:
        del os.environ['APP_VERSION'] # Remove if it wasn't set originally


# --- Test Cases ---

def test_hello_world(client):
    """
    Tests the root ('/') endpoint.
    Verifies HTTP status code and expected greeting including the mocked version.
    """
    rv = client.get('/') # Make a GET request to the root URL
    assert rv.status_code == 200 # Assert HTTP 200 OK
    # Assert that the response data contains the expected byte string including the mocked version
    assert b'Hello, Flask in Docker! This is version: test-version-1.0.0' in rv.data
    assert rv.mimetype == 'text/html' # Typically Flask returns text/html for simple strings

def test_status_endpoint(client):
    """
    Tests the '/status' endpoint.
    Verifies HTTP status code and that it returns 'OK'.
    """
    rv = client.get('/status') # Make a GET request to the /status URL
    assert rv.status_code == 200 # Assert HTTP 200 OK
    assert b'OK' in rv.data
    assert rv.mimetype == 'text/html'

def test_health_endpoint_success(client):
    """
    Tests the '/health' endpoint for a successful response.
    Verifies HTTP status code, JSON format, and essential health attributes.
    """
    rv = client.get('/health') # Make a GET request to the /health URL
    assert rv.status_code == 200 # Assert HTTP 200 OK
    assert rv.mimetype == 'application/json' # Assert response is JSON

    data = json.loads(rv.data) # Parse the JSON response

    # Assert basic structure and expected values
    assert isinstance(data, dict)
    assert 'status' in data
    assert 'timestamp' in data
    assert 'application_version' in data
    assert 'environment' in data
    assert 'checks' in data # Even if empty, the key should exist

    assert data['status'] == 'UP' # Assuming no external dependencies are mocked as down
    assert data['application_version'] == 'test-version-1.0.0'
    assert data['environment'] == 'testing' # Confirm it picked up the testing environment
    assert isinstance(data['timestamp'], str) # Check if timestamp is a string
    assert isinstance(data['checks'], list)

# Example of a test for degraded/down health (requires mocking dependencies)
# For instance, if your /health endpoint checks a database, you would mock the
# database connection to simulate a failure and then assert the 'DOWN' status.
# @pytest.mark.parametrize("db_up, expected_status", [(True, "UP"), (False, "DOWN")])
# def test_health_endpoint_with_mocked_db(client, mocker, db_up, expected_status):
#     """
#     Tests the /health endpoint with a mocked database connection.
#     Requires pytest-mock (pip install pytest-mock).
#     """
#     # Mock the internal function that checks the database
#     mocker.patch('app.check_database_connection', return_value=(db_up, "Mocked DB status"))
#
#     rv = client.get('/health')
#     data = json.loads(rv.data)
#
#     assert data['status'] == expected_status
#     if not db_up:
#         assert rv.status_code == 503 # Or 200 if DEGRADED is allowed for non-critical failures
#     else:
#         assert rv.status_code == 200
#     assert any(c['name'] == 'database' and c['status'] == ('OK' if db_up else 'DOWN') for c in data['checks'])

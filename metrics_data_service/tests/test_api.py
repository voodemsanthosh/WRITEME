import os
from unittest.mock import patch
# Note: TestClient and app import moved into test functions after patching.

# Define the mock environment variables needed for database.py to load
MOCK_DB_ENV = {
    "DB_SERVER": "test_server",
    "DB_NAME": "test_db",
    "DB_USER": "test_user",
    "DB_PASSWORD": "test_password"
    # DB_PORT and DB_DRIVER will use defaults from database.py
}

@patch.dict(os.environ, MOCK_DB_ENV)
def test_get_metrics_data_endpoint():
    """
    Test the /api/v1/metrics-data endpoint.
    It should return a 200 OK and a list (even if empty).
    """
    # Imports moved inside to ensure os.environ is patched before 'database.py' is loaded
    # when 'main' and then 'app' are imported.
    from fastapi.testclient import TestClient
    from main import app # metrics_data_service.main

    client = TestClient(app)
    response = client.get("/api/v1/metrics-data")
    assert response.status_code == 200
    # The actual data returned depends on the database state,
    # but it should always be a list according to the response_model.
    # For this test, since the DB connection is mocked at a higher level by TestClient
    # or if it were a real but empty test DB, an empty list is expected.
    # If testing against a real (mocked) DB that is not actually reachable,
    # the endpoint might fail if it tries to connect.
    # However, TestClient often bypasses actual network calls for FastAPI apps.
    # The primary goal here is to ensure the app loads with env vars.
    assert isinstance(response.json(), list)

@patch.dict(os.environ, MOCK_DB_ENV)
def test_root_endpoint():
    """
    Test the root / endpoint.
    """
    from fastapi.testclient import TestClient
    from main import app

    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Metrics Data Service. Navigate to /docs for API documentation."}

# TODO: Add more tests:
# - Test creating a metric (POST /api/v1/metrics/) and then retrieving it.
# - Test retrieving a specific metric by ID (GET /api/v1/metrics/{metric_id}).
# - Test with various query parameters (skip, limit).
# - Test for non-existent metric ID (should return 404).
# - Test with invalid data for POST requests.
# These more complex tests would require managing test database state
# or mocking database interactions effectively.

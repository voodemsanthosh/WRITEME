from fastapi.testclient import TestClient
# Assuming pytest is run from the 'metrics_data_service' directory,
# and 'main.py' is in that directory.
from main import app # Corrected import path based on typical pytest execution

client = TestClient(app)

def test_get_metrics_data_endpoint():
    """
    Test the /api/v1/metrics-data endpoint.
    It should return a 200 OK and a list (even if empty).
    """
    response = client.get("/api/v1/metrics-data")
    assert response.status_code == 200
    # The actual data returned depends on the database state,
    # but it should always be a list according to the response_model.
    assert isinstance(response.json(), list)

def test_root_endpoint():
    """
    Test the root / endpoint.
    """
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

import os
from unittest.mock import MagicMock 

# Define and apply mock environment variables BEFORE any application imports.
MOCK_DB_ENV_API = {
    "DB_SERVER": "test_server_api_final",
    "DB_NAME": "test_db_api_final",
    "DB_USER": "test_user_api_final",
    "DB_PASSWORD": "test_password_api_final",
    "DB_PORT": "1433", 
    "DB_DRIVER": "ODBC Driver 18 for SQL Server"
}
os.environ.update(MOCK_DB_ENV_API)

# create_engine and metadata.create_all are now expected to be patched by conftest.py

from fastapi.testclient import TestClient
from metrics_data_service.main import app 
# Import dependencies to override get_db for specific tests
from metrics_data_service.src import dependencies 
from metrics_data_service.src.models import Metric as SQLModelMetric # For type hints if needed by mock

client = TestClient(app)

def test_get_metrics_data_endpoint():
    """
    Test the /api/v1/metrics-data endpoint by overriding the DB dependency.
    """
    # Create a mock session
    mock_db_session = MagicMock()
    
    # Configure the mock session's query chain to return an empty list for this test
    mock_query_result = MagicMock()
    # Example: if crud.get_metrics returns a list of SQLAlchemy models,
    # and they are converted to Pydantic models by the endpoint.
    # For an empty list, this detailed mocking of query might not even be hit
    # if the list is empty early, but good for structure.
    mock_query_result.offset.return_value.limit.return_value.all.return_value = [] 
    mock_db_session.query.return_value = mock_query_result

    # Override the get_db dependency to return our mock_db_session
    app.dependency_overrides[dependencies.get_db] = lambda: mock_db_session
    
    response = client.get("/api/v1/metrics-data")
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    # If crud.get_metrics returns an empty list, the endpoint should return an empty list.
    assert response.json() == [] 

    # Clean up the dependency override to not affect other tests
    del app.dependency_overrides[dependencies.get_db]

def test_root_endpoint():
    """
    Test the root / endpoint. This endpoint does not use the database.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Metrics Data Service. Navigate to /docs for API documentation."}

# TODO: Add more tests:
# - Test /api/v1/metrics-data with data returned (configure mock_db_session to return mock Metric objects)
# - Test POST /api/v1/metrics/ (override get_db, mock crud.create_metric)
# - Test GET /api/v1/metrics/{metric_id} (override get_db, mock crud.get_metric)

def tearDownModule():
    """Clean up environment variables set by this module."""
    for key in MOCK_DB_ENV_API:
        if os.environ.get(key) == MOCK_DB_ENV_API[key]:
            del os.environ[key]

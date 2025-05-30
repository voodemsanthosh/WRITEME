import os
import pytest
from unittest.mock import patch, MagicMock

MOCK_DB_ENV_FOR_SESSION = {
    "DB_SERVER": "mock_server_for_session",
    "DB_NAME": "mock_db_for_session",
    "DB_USER": "mock_user_for_session",
    "DB_PASSWORD": "mock_password_for_session",
    "DB_PORT": "1433", 
    "DB_DRIVER": "ODBC Driver 18 for SQL Server"
}

@pytest.fixture(scope='session', autouse=True)
def mock_db_environment_for_session():
    """
    Patches os.environ for the entire test session using clear=True
    to ensure a controlled environment.
    """
    # The 'clear=True' argument ensures that the test environment starts clean,
    # only containing the MOCK_DB_ENV_FOR_SESSION variables.
    with patch.dict(os.environ, MOCK_DB_ENV_FOR_SESSION, clear=True):
        yield

@pytest.fixture(scope='session', autouse=True)
def mock_sqlalchemy_and_metadata_for_session(mock_db_environment_for_session):
    """
    This fixture depends on the environment being set by mock_db_environment_for_session.
    It mocks:
    1. `sqlalchemy.create_engine` within `metrics_data_service.src.database`
    2. `Base.metadata.create_all` within `metrics_data_service.src.models` (used by main.py's lifespan)
    This prevents any real database operations or attempts to load ODBC drivers.
    """
    # Patch create_engine where it's defined and used to create database.engine
    with patch('metrics_data_service.src.database.create_engine') as mock_create_engine, \
         patch('metrics_data_service.src.models.Base.metadata.create_all') as mock_metadata_create_all:
        
        mock_engine_instance = MagicMock(name="MockEngineInstance")
        # Configure the mock engine to handle typical engine operations if needed by app startup
        mock_connection = MagicMock(name="MockConnection")
        mock_transaction = MagicMock(name="MockTransaction") # For 'with conn.begin():'
        mock_connection.__enter__.return_value = mock_transaction # For 'with engine.connect() as conn:'
        mock_engine_instance.connect.return_value = mock_connection
        
        mock_create_engine.return_value = mock_engine_instance
        
        # mock_metadata_create_all is already a MagicMock.
        # It will capture calls if main.py's lifespan event tries to call it.
        
        # Yielding the mocks allows tests to access them if needed,
        # though for autouse session fixtures, this is less common for direct test use.
        yield {
            "mock_create_engine": mock_create_engine,
            "mock_engine_instance": mock_engine_instance,
            "mock_metadata_create_all": mock_metadata_create_all
        }
        # Patchers are automatically stopped when the 'with' block exits (end of session).

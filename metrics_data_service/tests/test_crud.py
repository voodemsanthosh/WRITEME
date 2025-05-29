import unittest
from unittest.mock import MagicMock, patch
import os

# Define and apply mock environment variables BEFORE src imports
# This is crucial because src.models (imported by src.crud) imports src.database,
# which checks environment variables upon its module load.
MOCK_DB_ENV = {
    "DB_SERVER": "test_server_crud", # Use different values to distinguish if needed
    "DB_NAME": "test_db_crud",
    "DB_USER": "test_user_crud",
    "DB_PASSWORD": "test_password_crud"
}
# Apply the patch globally for this module.
# For more complex scenarios, setUpModule/tearDownModule with patcher.start/stop might be used.
os.environ.update(MOCK_DB_ENV)

# Now, import modules from 'src'. These will see the patched environment.
from src.crud import get_metrics
from src.models import Metric as SQLModelMetric
from src.schemas import Metric as PydanticMetric

class TestCrudOperations(unittest.TestCase):
    # No need to patch os.environ again here if done globally for the module,
    # or if using setUpModule with patcher.start().

    def test_get_metrics_empty(self):
        """Test get_metrics when the database returns no metrics."""
        mock_db_session = MagicMock()
        
        # Mock the chain of SQLAlchemy calls
        mock_query_result = MagicMock()
        mock_query_result.offset.return_value.limit.return_value.all.return_value = []
        
        mock_db_session.query.return_value = mock_query_result
        
        result = get_metrics(db=mock_db_session, skip=0, limit=10)
        
        self.assertEqual(result, [])
        mock_db_session.query.assert_called_once_with(SQLModelMetric)
        mock_query_result.offset.assert_called_once_with(0)
        mock_query_result.limit.assert_called_once_with(10)
        mock_query_result.offset.return_value.limit.return_value.all.assert_called_once()

    def test_get_metrics_with_data(self):
        """Test get_metrics when the database returns some metrics."""
        mock_db_session = MagicMock()
        
        # Prepare mock Metric model instances (SQLAlchemy model instances)
        mock_metric_1 = SQLModelMetric(id=1, name="cpu_usage", value=0.75, source="server1")
        mock_metric_2 = SQLModelMetric(id=2, name="memory_usage", value=0.55, source="server1")
        expected_metrics = [mock_metric_1, mock_metric_2]

        mock_query_result = MagicMock()
        mock_query_result.offset.return_value.limit.return_value.all.return_value = expected_metrics
        
        mock_db_session.query.return_value = mock_query_result
        
        result = get_metrics(db=mock_db_session, skip=0, limit=10)
        
        self.assertEqual(result, expected_metrics)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].name, "cpu_usage")
        mock_db_session.query.assert_called_once_with(SQLModelMetric)
        mock_query_result.offset.assert_called_once_with(0)
        mock_query_result.limit.assert_called_once_with(10)
        mock_query_result.offset.return_value.limit.return_value.all.assert_called_once()

    # TODO: Add tests for create_metric
    # This would involve:
    # - Mocking db.add, db.commit, db.refresh
    # - Verifying these methods are called with the correct Metric object.
    # - Ensuring the input Pydantic schema is correctly mapped to the SQLAlchemy model.

    # TODO: Add tests for get_metric (single metric by ID)
    # This would involve:
    # - Mocking db.query(...).filter(...).first()
    # - Testing cases where a metric is found and where it's not found.

if __name__ == '__main__':
    unittest.main()

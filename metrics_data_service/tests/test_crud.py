import unittest
from unittest.mock import MagicMock, patch

# Assuming pytest is run from the 'metrics_data_service' directory
from src.crud import get_metrics
from src.models import Metric as SQLModelMetric # Alias to avoid Pydantic/SQLModel name clash if any
from src.schemas import Metric as PydanticMetric # For creating test data

class TestCrudOperations(unittest.TestCase):

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

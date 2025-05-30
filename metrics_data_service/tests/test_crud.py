import unittest
from unittest.mock import MagicMock 
# os and patch are no longer needed here for environment setup or create_engine mocking,
# as conftest.py now handles these for the entire session.

# Imports should now be safe at module level due to conftest.py's session-wide patches.
from metrics_data_service.src.crud import get_metrics
from metrics_data_service.src.models import Metric as SQLModelMetric

class TestCrudOperations(unittest.TestCase):

    def test_get_metrics_empty(self):
        """Test get_metrics when the database returns no metrics."""
        mock_db_session = MagicMock()
        
        mock_query_result = MagicMock()
        mock_query_result.offset.return_value.limit.return_value.all.return_value = []
        
        mock_db_session.query.return_value = mock_query_result
        
        result = get_metrics(db=mock_db_session, skip=0, limit=10)
        
        self.assertEqual(result, [])
        mock_db_session.query.assert_called_once_with(SQLModelMetric)
        mock_query_result.offset.assert_called_once_with(0)
        mock_query_result.offset.return_value.limit.assert_called_once_with(10)
        mock_query_result.offset.return_value.limit.return_value.all.assert_called_once()

    def test_get_metrics_with_data(self):
        """Test get_metrics when the database returns some metrics."""
        mock_db_session = MagicMock()
        
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
        mock_query_result.offset.return_value.limit.assert_called_once_with(10)
        mock_query_result.offset.return_value.limit.return_value.all.assert_called_once()

    # TODO: Add tests for create_metric, get_metric

if __name__ == '__main__':
    unittest.main()

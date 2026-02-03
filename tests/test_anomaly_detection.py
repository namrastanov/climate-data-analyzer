"""Tests for anomaly detection module."""

import pytest
import numpy as np
from climate_data_analyzer.analysis.anomaly_detection import AnomalyDetector, Anomaly


class TestAnomalyDetector:
    """Test suite for AnomalyDetector."""

    @pytest.fixture
    def detector(self):
        """Create detector instance."""
        return AnomalyDetector(contamination=0.1)

    @pytest.fixture
    def normal_data(self):
        """Generate normal distribution data."""
        np.random.seed(42)
        return np.random.normal(0, 1, 100)

    @pytest.fixture
    def data_with_outliers(self):
        """Generate data with known outliers."""
        np.random.seed(42)
        data = np.random.normal(0, 1, 100)
        data[10] = 10.0
        data[50] = -10.0
        return data

    def test_iqr_detects_outliers(self, detector, data_with_outliers):
        """Test IQR method detects known outliers."""
        anomalies = detector.detect_iqr(data_with_outliers)
        indices = [a.index for a in anomalies]
        assert 10 in indices
        assert 50 in indices

    def test_zscore_detects_outliers(self, detector, data_with_outliers):
        """Test Z-score method detects known outliers."""
        anomalies = detector.detect_zscore(data_with_outliers, threshold=3.0)
        indices = [a.index for a in anomalies]
        assert 10 in indices
        assert 50 in indices

    def test_isolation_forest_detects_outliers(self, detector, data_with_outliers):
        """Test Isolation Forest detects outliers."""
        anomalies = detector.detect_isolation_forest(data_with_outliers)
        assert len(anomalies) > 0

    def test_normal_data_few_anomalies(self, detector, normal_data):
        """Test that normal data has few anomalies."""
        anomalies = detector.detect_zscore(normal_data, threshold=3.0)
        assert len(anomalies) < 5

    def test_anomaly_has_required_fields(self, detector, data_with_outliers):
        """Test Anomaly dataclass has all fields."""
        anomalies = detector.detect_iqr(data_with_outliers)
        if anomalies:
            a = anomalies[0]
            assert hasattr(a, "index")
            assert hasattr(a, "value")
            assert hasattr(a, "score")
            assert hasattr(a, "method")

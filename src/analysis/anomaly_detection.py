"""Statistical anomaly detection for climate data."""

import numpy as np
import pandas as pd
from typing import List, Tuple, Optional
from sklearn.ensemble import IsolationForest
from dataclasses import dataclass


@dataclass
class Anomaly:
    """Represents a detected anomaly."""
    index: int
    value: float
    score: float
    method: str
    timestamp: Optional[str] = None


class AnomalyDetector:
    """Multi-method anomaly detection for climate data."""

    def __init__(self, contamination: float = 0.05):
        self.contamination = contamination
        self._isolation_forest: Optional[IsolationForest] = None

    def detect_iqr(
        self,
        data: np.ndarray,
        multiplier: float = 1.5
    ) -> List[Anomaly]:
        """Detect anomalies using IQR method."""
        q1, q3 = np.percentile(data, [25, 75])
        iqr = q3 - q1
        lower = q1 - multiplier * iqr
        upper = q3 + multiplier * iqr
        
        anomalies = []
        for i, value in enumerate(data):
            if value < lower or value > upper:
                score = abs(value - np.median(data)) / iqr
                anomalies.append(Anomaly(i, value, score, "IQR"))
        
        return anomalies

    def detect_zscore(
        self,
        data: np.ndarray,
        threshold: float = 3.0
    ) -> List[Anomaly]:
        """Detect anomalies using Z-score method."""
        mean = np.mean(data)
        std = np.std(data)
        
        if std == 0:
            return []
        
        anomalies = []
        for i, value in enumerate(data):
            zscore = abs(value - mean) / std
            if zscore > threshold:
                anomalies.append(Anomaly(i, value, zscore, "Z-score"))
        
        return anomalies

    def detect_isolation_forest(
        self,
        data: np.ndarray
    ) -> List[Anomaly]:
        """Detect anomalies using Isolation Forest."""
        if data.ndim == 1:
            data = data.reshape(-1, 1)
        
        self._isolation_forest = IsolationForest(
            contamination=self.contamination,
            random_state=42
        )
        
        predictions = self._isolation_forest.fit_predict(data)
        scores = self._isolation_forest.score_samples(data)
        
        anomalies = []
        for i, (pred, score) in enumerate(zip(predictions, scores)):
            if pred == -1:
                anomalies.append(Anomaly(
                    i, data[i, 0] if data.ndim > 1 else data[i],
                    abs(score), "IsolationForest"
                ))
        
        return anomalies

    def detect_all(
        self,
        data: np.ndarray
    ) -> dict[str, List[Anomaly]]:
        """Run all detection methods."""
        return {
            "iqr": self.detect_iqr(data),
            "zscore": self.detect_zscore(data),
            "isolation_forest": self.detect_isolation_forest(data)
        }

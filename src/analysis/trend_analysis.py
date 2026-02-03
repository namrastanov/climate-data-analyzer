"""Long-term climate trend analysis."""

import numpy as np
from typing import Tuple, Optional
from dataclasses import dataclass
from scipy import stats


@dataclass
class TrendResult:
    """Results of trend analysis."""
    slope: float
    intercept: float
    p_value: float
    trend_direction: str
    is_significant: bool
    confidence_interval: Tuple[float, float]


class TrendAnalyzer:
    """Analyzer for long-term climate trends."""

    def __init__(self, significance_level: float = 0.05):
        self.significance_level = significance_level

    def mann_kendall_test(
        self,
        data: np.ndarray
    ) -> Tuple[float, float, str]:
        """Perform Mann-Kendall trend test."""
        n = len(data)
        s = 0
        
        for i in range(n - 1):
            for j in range(i + 1, n):
                diff = data[j] - data[i]
                if diff > 0:
                    s += 1
                elif diff < 0:
                    s -= 1
        
        var_s = (n * (n - 1) * (2 * n + 5)) / 18
        
        if s > 0:
            z = (s - 1) / np.sqrt(var_s)
        elif s < 0:
            z = (s + 1) / np.sqrt(var_s)
        else:
            z = 0
        
        p_value = 2 * (1 - stats.norm.cdf(abs(z)))
        
        if z > 0:
            trend = "increasing"
        elif z < 0:
            trend = "decreasing"
        else:
            trend = "no trend"
        
        return z, p_value, trend

    def sens_slope(self, data: np.ndarray) -> float:
        """Calculate Sen's slope estimator."""
        n = len(data)
        slopes = []
        
        for i in range(n - 1):
            for j in range(i + 1, n):
                slope = (data[j] - data[i]) / (j - i)
                slopes.append(slope)
        
        return np.median(slopes)

    def analyze(self, data: np.ndarray) -> TrendResult:
        """Perform complete trend analysis."""
        z_stat, p_value, direction = self.mann_kendall_test(data)
        slope = self.sens_slope(data)
        
        n = len(data)
        x = np.arange(n)
        intercept = np.median(data - slope * x)
        
        se = slope * np.sqrt((n * (n + 1) * (2 * n + 1)) / (6 * n * (n - 1)))
        ci = (
            slope - 1.96 * se,
            slope + 1.96 * se
        )
        
        return TrendResult(
            slope=slope,
            intercept=intercept,
            p_value=p_value,
            trend_direction=direction,
            is_significant=p_value < self.significance_level,
            confidence_interval=ci
        )

    def seasonal_decompose(
        self,
        data: np.ndarray,
        period: int = 12
    ) -> dict:
        """Simple seasonal decomposition."""
        n = len(data)
        
        trend = np.convolve(data, np.ones(period)/period, mode='same')
        
        detrended = data - trend
        seasonal = np.zeros(n)
        for i in range(period):
            indices = np.arange(i, n, period)
            seasonal[indices] = np.mean(detrended[indices])
        
        residual = data - trend - seasonal
        
        return {
            "trend": trend,
            "seasonal": seasonal,
            "residual": residual
        }

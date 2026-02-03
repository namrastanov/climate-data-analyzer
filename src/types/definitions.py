"""Type definitions for climate analyzer."""

from typing import TypedDict, List, Optional, Union
from datetime import datetime
import numpy as np
import pandas as pd


class ClimateRecord(TypedDict):
    """Type definition for climate data record."""
    timestamp: datetime
    station_id: str
    latitude: float
    longitude: float
    temperature: Optional[float]
    temperature_min: Optional[float]
    temperature_max: Optional[float]
    precipitation: Optional[float]
    humidity: Optional[float]
    pressure: Optional[float]
    wind_speed: Optional[float]
    wind_direction: Optional[float]


class AnalysisResult(TypedDict):
    """Type definition for analysis results."""
    analyzer: str
    timestamp: str
    parameters: dict
    metrics: dict
    data: Optional[dict]


class TrendMetrics(TypedDict):
    """Type definition for trend analysis metrics."""
    slope: float
    p_value: float
    trend_direction: str
    is_significant: bool
    confidence_interval: tuple


ArrayLike = Union[np.ndarray, pd.Series, List[float]]
DateLike = Union[str, datetime, pd.Timestamp]


class DataQualityReport(TypedDict):
    """Type definition for data quality report."""
    total_records: int
    null_counts: dict
    null_percentages: dict
    outlier_counts: dict
    date_range: tuple
    stations: List[str]

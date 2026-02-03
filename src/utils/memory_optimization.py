"""Memory optimization utilities for large datasets."""

import pandas as pd
import numpy as np
from typing import Dict, Optional, Iterator
import logging

logger = logging.getLogger(__name__)


def optimize_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """Optimize dataframe memory by downcasting dtypes."""
    optimized = df.copy()
    
    for col in optimized.select_dtypes(include=["int64"]).columns:
        col_min = optimized[col].min()
        col_max = optimized[col].max()
        
        if col_min >= 0:
            if col_max < 255:
                optimized[col] = optimized[col].astype(np.uint8)
            elif col_max < 65535:
                optimized[col] = optimized[col].astype(np.uint16)
            elif col_max < 4294967295:
                optimized[col] = optimized[col].astype(np.uint32)
        else:
            if col_min > -128 and col_max < 127:
                optimized[col] = optimized[col].astype(np.int8)
            elif col_min > -32768 and col_max < 32767:
                optimized[col] = optimized[col].astype(np.int16)
            elif col_min > -2147483648 and col_max < 2147483647:
                optimized[col] = optimized[col].astype(np.int32)
    
    for col in optimized.select_dtypes(include=["float64"]).columns:
        optimized[col] = pd.to_numeric(optimized[col], downcast="float")
    
    for col in optimized.select_dtypes(include=["object"]).columns:
        num_unique = optimized[col].nunique()
        num_total = len(optimized[col])
        if num_unique / num_total < 0.5:
            optimized[col] = optimized[col].astype("category")
    
    return optimized


def read_chunked(
    filepath: str,
    chunk_size: int = 100000,
    optimize: bool = True
) -> Iterator[pd.DataFrame]:
    """Read large file in memory-efficient chunks."""
    for chunk in pd.read_csv(filepath, chunksize=chunk_size):
        if optimize:
            chunk = optimize_dtypes(chunk)
        yield chunk


def get_memory_usage(df: pd.DataFrame) -> Dict[str, float]:
    """Get detailed memory usage statistics."""
    total = df.memory_usage(deep=True).sum()
    by_column = df.memory_usage(deep=True).to_dict()
    
    return {
        "total_mb": total / (1024 * 1024),
        "by_column_mb": {k: v / (1024 * 1024) for k, v in by_column.items()},
        "rows": len(df),
        "columns": len(df.columns)
    }


class MemoryProfiler:
    """Profile memory usage during operations."""

    def __init__(self):
        self._snapshots: list = []

    def snapshot(self, label: str, df: pd.DataFrame) -> None:
        """Take memory snapshot."""
        usage = get_memory_usage(df)
        self._snapshots.append({"label": label, **usage})
        logger.info(f"Memory snapshot '{label}': {usage['total_mb']:.2f} MB")

    def report(self) -> pd.DataFrame:
        """Generate memory report."""
        return pd.DataFrame(self._snapshots)

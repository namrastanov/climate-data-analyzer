"""Data transformation utilities."""

import pandas as pd
import numpy as np
from typing import Callable, List, Optional
from abc import ABC, abstractmethod


class BaseTransformer(ABC):
    """Abstract base transformer."""

    @abstractmethod
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transform dataframe."""
        pass

    def __call__(self, df: pd.DataFrame) -> pd.DataFrame:
        """Allow transformer to be called directly."""
        return self.transform(df)


class DropNullsTransformer(BaseTransformer):
    """Drop rows with null values."""

    def __init__(self, columns: Optional[List[str]] = None, threshold: float = 0.5):
        self.columns = columns
        self.threshold = threshold

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Drop rows exceeding null threshold."""
        cols = self.columns or df.columns
        null_ratio = df[cols].isnull().sum(axis=1) / len(cols)
        return df[null_ratio < self.threshold].copy()


class InterpolateTransformer(BaseTransformer):
    """Interpolate missing values."""

    def __init__(self, method: str = "linear", columns: Optional[List[str]] = None):
        self.method = method
        self.columns = columns

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Interpolate missing values."""
        df = df.copy()
        cols = self.columns or df.select_dtypes(include=[np.number]).columns
        df[cols] = df[cols].interpolate(method=self.method)
        return df


class UnitConversionTransformer(BaseTransformer):
    """Convert measurement units."""

    CONVERSIONS = {
        "f_to_c": lambda x: (x - 32) * 5 / 9,
        "c_to_f": lambda x: x * 9 / 5 + 32,
        "mm_to_in": lambda x: x / 25.4,
        "in_to_mm": lambda x: x * 25.4,
    }

    def __init__(self, column: str, conversion: str):
        self.column = column
        self.conversion = conversion

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply unit conversion."""
        df = df.copy()
        func = self.CONVERSIONS.get(self.conversion)
        if func is None:
            raise ValueError(f"Unknown conversion: {self.conversion}")
        df[self.column] = df[self.column].apply(func)
        return df


class Pipeline:
    """Transformation pipeline."""

    def __init__(self, transformers: Optional[List[BaseTransformer]] = None):
        self.transformers = transformers or []

    def add(self, transformer: BaseTransformer) -> "Pipeline":
        """Add transformer to pipeline."""
        self.transformers.append(transformer)
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply all transformers."""
        result = df
        for transformer in self.transformers:
            result = transformer.transform(result)
        return result

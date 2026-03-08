"""Base class for analysis modules."""

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Optional
import logging
import pandas as pd

logger = logging.getLogger(__name__)


class BaseAnalyzer(ABC):
    """Abstract base class for all analyzers."""

    def __init__(self, name: str):
        self.name = name
        self._results: Optional[Dict[str, Any]] = None

    @abstractmethod
    def analyze(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Perform analysis on data."""
        pass

    @abstractmethod
    def validate_input(self, data: pd.DataFrame) -> bool:
        """Validate input data."""
        pass

    def run(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Execute analysis with validation."""
        logger.info(f"Running {self.name} analysis")
        
        if not self.validate_input(data):
            raise ValueError("Input validation failed")
        
        self._results = self.analyze(data)
        return self._results

    @property
    def results(self) -> Optional[Dict[str, Any]]:
        """Get analysis results."""
        return self._results

    def to_dataframe(self) -> pd.DataFrame:
        """Convert results to DataFrame."""
        if self._results is None:
            raise ValueError("No results available")
        return pd.DataFrame([self._results])


class AnalyzerRegistry:
    """Registry for analyzer plugins."""

    _analyzers: Dict[str, type] = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._analyzers = {}

    @classmethod
    def register(cls, name: str) -> Callable[[type], type]:
        """Decorator to register analyzer."""
        def wrapper(analyzer_cls: type) -> type:
            if not issubclass(analyzer_cls, BaseAnalyzer):
                raise TypeError(
                    f"Cannot register {analyzer_cls.__name__}: "
                    f"must be a subclass of BaseAnalyzer"
                )
            cls._analyzers[name] = analyzer_cls
            return analyzer_cls
        return wrapper

    @classmethod
    def get(cls, name: str) -> type:
        """Get analyzer class by name."""
        if name not in cls._analyzers:
            raise KeyError(f"Unknown analyzer: {name}")
        return cls._analyzers[name]

    @classmethod
    def list_analyzers(cls) -> list[str]:
        """List registered analyzers."""
        return list(cls._analyzers.keys())
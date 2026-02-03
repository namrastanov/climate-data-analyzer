"""Export utilities for analysis results."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Dict, Any
import pandas as pd
import json
import logging

logger = logging.getLogger(__name__)


class BaseExporter(ABC):
    """Abstract base exporter."""

    def __init__(self, output_dir: Path):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    def export(
        self,
        data: pd.DataFrame,
        filename: str,
        **kwargs
    ) -> Path:
        """Export data to file."""
        pass


class CSVExporter(BaseExporter):
    """Export to CSV format."""

    def export(
        self,
        data: pd.DataFrame,
        filename: str,
        delimiter: str = ",",
        **kwargs
    ) -> Path:
        """Export to CSV."""
        output_path = self.output_dir / f"{filename}.csv"
        data.to_csv(output_path, sep=delimiter, index=False, **kwargs)
        logger.info(f"Exported {len(data)} rows to {output_path}")
        return output_path


class ExcelExporter(BaseExporter):
    """Export to Excel format."""

    def export(
        self,
        data: pd.DataFrame,
        filename: str,
        sheet_name: str = "Data",
        **kwargs
    ) -> Path:
        """Export to Excel."""
        output_path = self.output_dir / f"{filename}.xlsx"
        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
            data.to_excel(writer, sheet_name=sheet_name, index=False, **kwargs)
        logger.info(f"Exported {len(data)} rows to {output_path}")
        return output_path


class ParquetExporter(BaseExporter):
    """Export to Parquet format."""

    def export(
        self,
        data: pd.DataFrame,
        filename: str,
        compression: str = "snappy",
        **kwargs
    ) -> Path:
        """Export to Parquet."""
        output_path = self.output_dir / f"{filename}.parquet"
        data.to_parquet(output_path, compression=compression, index=False, **kwargs)
        logger.info(f"Exported {len(data)} rows to {output_path}")
        return output_path


class JSONExporter(BaseExporter):
    """Export to JSON format."""

    def export(
        self,
        data: pd.DataFrame,
        filename: str,
        orient: str = "records",
        **kwargs
    ) -> Path:
        """Export to JSON."""
        output_path = self.output_dir / f"{filename}.json"
        data.to_json(output_path, orient=orient, **kwargs)
        logger.info(f"Exported {len(data)} rows to {output_path}")
        return output_path


class ExporterFactory:
    """Factory for creating exporters."""

    _exporters = {
        "csv": CSVExporter,
        "excel": ExcelExporter,
        "parquet": ParquetExporter,
        "json": JSONExporter
    }

    @classmethod
    def create(cls, format: str, output_dir: Path) -> BaseExporter:
        """Create exporter for given format."""
        if format not in cls._exporters:
            raise ValueError(f"Unknown format: {format}")
        return cls._exporters[format](output_dir)

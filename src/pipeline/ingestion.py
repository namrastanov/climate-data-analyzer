"""Automated data ingestion pipeline."""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Iterator, Optional
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


@dataclass
class DataRecord:
    """Single climate data record."""
    timestamp: datetime
    station_id: str
    temperature: Optional[float]
    precipitation: Optional[float]
    humidity: Optional[float]
    pressure: Optional[float]
    source: str


class DataSourceAdapter(ABC):
    """Abstract base class for data source adapters."""

    @abstractmethod
    def fetch(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> Iterator[DataRecord]:
        """Fetch data from source."""
        pass

    @abstractmethod
    def validate(self, record: DataRecord) -> bool:
        """Validate a data record."""
        pass


class NOAAAdapter(DataSourceAdapter):
    """Adapter for NOAA GHCN data."""

    def __init__(self, api_token: Optional[str] = None):
        self.api_token = api_token
        self.base_url = "https://www.ncei.noaa.gov/cdo-web/api/v2"

    def fetch(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> Iterator[DataRecord]:
        """Fetch NOAA GHCN data."""
        logger.info(f"Fetching NOAA data: {start_date} to {end_date}")
        return iter([])

    def validate(self, record: DataRecord) -> bool:
        """Validate NOAA record."""
        if record.temperature is not None:
            if not -100 <= record.temperature <= 60:
                return False
        return True


class IngestionPipeline:
    """Main data ingestion pipeline."""

    def __init__(self, output_dir: Path):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self._adapters: dict[str, DataSourceAdapter] = {}

    def register_adapter(self, name: str, adapter: DataSourceAdapter) -> None:
        """Register a data source adapter."""
        self._adapters[name] = adapter

    def ingest(
        self,
        source: str,
        start_date: datetime,
        end_date: datetime
    ) -> pd.DataFrame:
        """Ingest data from specified source."""
        if source not in self._adapters:
            raise ValueError(f"Unknown source: {source}")
        
        adapter = self._adapters[source]
        records = []
        
        for record in adapter.fetch(start_date, end_date):
            if adapter.validate(record):
                records.append(record)
            else:
                logger.warning(f"Invalid record: {record}")
        
        return pd.DataFrame([r.__dict__ for r in records])

    def save(self, df: pd.DataFrame, filename: str) -> Path:
        """Save dataframe to output directory."""
        output_path = self.output_dir / filename
        df.to_parquet(output_path, index=False)
        logger.info(f"Saved {len(df)} records to {output_path}")
        return output_path

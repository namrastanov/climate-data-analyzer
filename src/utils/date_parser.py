"""Robust date parsing for historical data."""

from datetime import datetime, date
from typing import Optional, List, Union
import re
import logging

logger = logging.getLogger(__name__)


class DateParser:
    """Parser for various date formats in historical data."""

    FORMATS = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%m/%d/%Y",
        "%Y%m%d",
        "%d-%m-%Y",
        "%Y/%m/%d",
        "%d %b %Y",
        "%d %B %Y",
        "%b %d, %Y",
        "%B %d, %Y",
    ]

    def __init__(self, preferred_format: Optional[str] = None):
        self.preferred_format = preferred_format
        self._format_cache: dict = {}

    def parse(
        self,
        date_str: str,
        day_first: bool = True
    ) -> Optional[datetime]:
        """Parse date string with multiple format attempts."""
        date_str = date_str.strip()
        
        if date_str in self._format_cache:
            fmt = self._format_cache[date_str]
            return datetime.strptime(date_str, fmt)
        
        if self.preferred_format:
            try:
                result = datetime.strptime(date_str, self.preferred_format)
                self._format_cache[date_str] = self.preferred_format
                return result
            except ValueError:
                pass
        
        formats = self._get_ordered_formats(day_first)
        for fmt in formats:
            try:
                result = datetime.strptime(date_str, fmt)
                self._format_cache[date_str] = fmt
                return result
            except ValueError:
                continue
        
        logger.warning(f"Could not parse date: {date_str}")
        return None

    def _get_ordered_formats(self, day_first: bool) -> List[str]:
        """Get formats ordered by preference."""
        if day_first:
            return [f for f in self.FORMATS if "d" in f[:3]] +                    [f for f in self.FORMATS if "d" not in f[:3]]
        return [f for f in self.FORMATS if "m" in f[:3]] +                [f for f in self.FORMATS if "m" not in f[:3]]

    def parse_julian(self, year: int, day_of_year: int) -> datetime:
        """Parse Julian day number."""
        return datetime(year, 1, 1) + timedelta(days=day_of_year - 1)

    def validate(self, dt: datetime) -> bool:
        """Validate parsed date is reasonable."""
        min_date = datetime(1800, 1, 1)
        max_date = datetime(2100, 12, 31)
        return min_date <= dt <= max_date

    def detect_format(self, samples: List[str]) -> Optional[str]:
        """Detect most likely format from samples."""
        format_counts: dict = {}
        
        for sample in samples[:100]:
            for fmt in self.FORMATS:
                try:
                    datetime.strptime(sample.strip(), fmt)
                    format_counts[fmt] = format_counts.get(fmt, 0) + 1
                except ValueError:
                    pass
        
        if format_counts:
            return max(format_counts.items(), key=lambda x: x[1])[0]
        return None


from datetime import timedelta

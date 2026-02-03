# climate-data-analyzer

![Python](https://img.shields.io/badge/python-3.10+-blue.svg) ![Coverage](https://img.shields.io/badge/coverage-85%25-yellowgreen.svg) ![Docs](https://img.shields.io/badge/docs-latest-blue.svg)

Comprehensive toolkit for analyzing climate patterns and generating insights from historical weather data


## Features

- **Anomaly Detection**: Statistical methods to identify unusual patterns
- **Trend Analysis**: Long-term climate trend identification with Mann-Kendall test
- **Data Pipeline**: Automated ingestion from NOAA, ERA5, and local stations
- **Visualization**: Interactive charts and maps for data exploration
- **Export Formats**: Support for CSV, Excel, Parquet, and NetCDF


## Installation

```bash
# Clone the repository
git clone https://github.com/{username}/climate-data-analyzer.git
cd climate-data-analyzer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

## Quick Start

```python
from climate_data_analyzer import main

# Initialize the application
app = main.create_app()

# Run the service
app.run()
```

## Configuration

Copy the example environment file and configure your settings:

```bash
cp .env.example .env
```

Key configuration options:
- `API_KEY`: Your API key for weather data providers
- `DATABASE_URL`: Database connection string
- `REDIS_URL`: Redis connection for caching
- `LOG_LEVEL`: Logging verbosity (DEBUG, INFO, WARNING, ERROR)

## Development

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run linting
ruff check .

# Format code
black .
```

## API Documentation

Once running, access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details.

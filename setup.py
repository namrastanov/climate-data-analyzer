"""Setup configuration for climate-data-analyzer."""

from setuptools import setup, find_packages

setup(
    name="climate-data-analyzer",
    version="0.1.0",
    description="Comprehensive toolkit for analyzing climate patterns and generating insights from historical weather data",
    author="Demo Author",
    author_email="demo@example.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    install_requires=[
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "scikit-learn>=1.3.0",
        "requests>=2.31.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "ruff>=0.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "climate-data-analyzer=climate_data_analyzer.main:main",
        ],
    },
)

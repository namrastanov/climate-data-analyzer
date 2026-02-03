"""Secure secrets management."""

import os
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class SecretsManager:
    """Manage sensitive credentials securely."""

    SECRETS_FILE = ".secrets"
    ENV_PREFIX = "CLIMATE_"

    def __init__(self, secrets_dir: Optional[Path] = None):
        self.secrets_dir = secrets_dir or Path.home() / ".climate-analyzer"
        self._secrets: dict = {}
        self._load_secrets()

    def _load_secrets(self) -> None:
        """Load secrets from file and environment."""
        secrets_file = self.secrets_dir / self.SECRETS_FILE
        
        if secrets_file.exists():
            with open(secrets_file) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        self._secrets[key.strip()] = value.strip()
        
        for key, value in os.environ.items():
            if key.startswith(self.ENV_PREFIX):
                secret_key = key[len(self.ENV_PREFIX):]
                self._secrets[secret_key] = value

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Get secret value."""
        return self._secrets.get(key, default)

    def require(self, key: str) -> str:
        """Get required secret, raise if missing."""
        value = self.get(key)
        if value is None:
            raise ValueError(f"Required secret not found: {key}")
        return value

    def set(self, key: str, value: str) -> None:
        """Set secret (in memory only)."""
        self._secrets[key] = value

    def validate_all(self, required_keys: list) -> bool:
        """Validate all required secrets exist."""
        missing = [k for k in required_keys if k not in self._secrets]
        if missing:
            logger.error(f"Missing required secrets: {missing}")
            return False
        return True

    @staticmethod
    def mask(value: str, visible_chars: int = 4) -> str:
        """Mask secret for logging."""
        if len(value) <= visible_chars:
            return "*" * len(value)
        return value[:visible_chars] + "*" * (len(value) - visible_chars)

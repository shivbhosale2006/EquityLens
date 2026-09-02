"""Environment-based application configuration."""

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    """Runtime settings loaded once from environment variables."""

    environment: str = "development"
    log_level: str = "INFO"
    cache_dir: Path = Path("data/raw")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached settings, allowing local values from an ignored .env file."""
    load_dotenv()
    return Settings(
        environment=os.getenv("EQUITYLENS_ENV", "development"),
        log_level=os.getenv("EQUITYLENS_LOG_LEVEL", "INFO").upper(),
        cache_dir=Path(os.getenv("EQUITYLENS_CACHE_DIR", "data/raw")),
    )

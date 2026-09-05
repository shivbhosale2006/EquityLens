"""Market-data providers Equitylens."""

from abc import ABC, abstractmethod

import pandas as pd
import yfinance as yf

STANDARD_COLUMNS = ["date", "open", "high", "low", "close", "volume"]


class MarketDataProvider(ABC):
    """Define the interface ever market data provider must follow."""

    @abstractmethod
    def get_daily_data(
        self,
        ticker: str,
        period: str = "5y",
    ) -> pd.DataFrame:
        """Return Standardised daily OHLCV data."""


class YahooFinanceProvider(MarketDataProvider):
    """Retrieve historical market data using yfinance."""

    def get_daily_data(
        self,
        ticker: str,
        period: str = "5y",
    ) -> pd.DataFrame:
        """Download and standardise daily market data."""

        raw_data = yf.download(
            tickers=ticker,
            period=period,
            interval="1d",
            auto_adjust=True,
            actions=False,
            progress=False,
            multi_level_index=False,
        )

        if raw_data.empty:
            raise ValueError(f"No market data returned for {ticker}")

        data = raw_data.reset_index()

        data = data.rename(
            columns={
                "Date": "date",
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
                "Volume": "volume",
            }
        )
        missing_columns = set(STANDARD_COLUMNS) - set(data.columns)

        if missing_columns:
            raise ValueError(f"Missing expected columns: {sorted(missing_columns)}")

        data = data[STANDARD_COLUMNS].copy()

        data["date"] = pd.to_datetime(data["date"], utc=True).dt.tz_convert(None)

        numeric_columns = ["open", "high", "low", "close", "volume"]

        for column in numeric_columns:
            data[column] = pd.to_numeric(data[column], errors="coerce")

        data = data.dropna(subset=STANDARD_COLUMNS)

        data = (
            data.drop_duplicates(subset="date", keep="last")
            .sort_values("date")
            .reset_index(drop=True)
        )

        return data

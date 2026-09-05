from __future__ import annotations

import pandas as pd

class MarketDataValidationError(ValueError):
    """Raised when market data fails validation."""

def normalise_ticker(ticker: str) ->str:
    """convert an ASX ticker into standard Yahoo Finance ticker."""

    if not isinstance(ticker, str):
        raise MarketDataValidationError("Ticker must be a string.")

    ticker = ticker.strip().upper()

    if not ticker:
        raise MarketDataValidationError("Ticker cannot be empty.")

    if "." not in ticker:
        ticker =f"{ticker}.AX"

    if not ticker.endswith(".AX"):
        raise MarketDataValidationError(f"Invalid ASX ticker: {ticker}")

    return ticker



def validate_market_data(
        data: pd.DataFrame,
        *,
        min_rows: int = 252,
) -> None:
    """Validate daily OHCLV market data."""

    if data.empty:
        raise MarketDataValidationError("Market data is empty.")

    required_columns= {
        "open",
        "high",
        "low",
        "close",
        "volume"
    }

    missing_columns = required_columns.difference(
        data.columns
    )

    if missing_columns:
        raise MarketDataValidationError(
            "Missing required columns:"f"{sorted(missing_columns)}"
        )

    if data.index.duplicated().any():
        raise MarketDataValidationError(
            "Market data contains duplicate dates."
        )

    if data[["open","high","low","close"]].isna().any.any():
        raise MarketDataValidationError(
            "Market data contains missing OHLC values"
        )

    if data["volume"].isna().any():
        raise MarketDataValidationError(
            "Market data contains missing volume values."
        )

    if (data["volume"] < 0).any():
        raise MarketDataValidationError(
            "Market data contains negative volume values."
        )

    invalid_high = (
        (data["high"] < data["open"])
        | (data["high"] < data["close"])
        | (data["high"]) < data["low"]
    )


    if invalid_high.any():
        raise MarketDataValidationError(
            "Market data contains invalid high prices."
        )

    invalid_low =(
        (data["low"]>data["open"])
        | (data["low"] > data["close"])
        | (data["low"] > data["high"])
    )

    if invalid_low.any():
        raise MarketDataValidationError(
            "Market data contains invalid low prices."
        )

    if len(data) < min_rows:
        raise MarketDataValidationError(
            f"Insufficient market history:"
            f"{len(data)} rows found,"
            f"at least {min_rows} required"
        )

    
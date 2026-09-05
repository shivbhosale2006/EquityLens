"""Download sample market data for the EquityLens prototype."""

from pathlib import Path

from equitylens.data.provider import STANDARD_COLUMNS, YahooFinanceProvider

TICKER = "DRO.AX"
PERIOD = "5y"
OUTPUT_PATH = Path("data/raw/dro_ax_daily.csv")


def validate_data(data) -> None:
    """Check that the downloaded data satisfies our requirements."""

    if list(data.columns) != STANDARD_COLUMNS:
        raise ValueError("The dataset does not have the expected columns.")

    if data.empty:
        raise ValueError("The downloaded dataset is empty.")

    if not data["date"].is_monotonic_increasing:
        raise ValueError("Dates are not sorted in ascending order.")

    if data["date"].duplicated().any():
        raise ValueError("The dataset contains duplicate dates.")

    if data.isna().any().any():
        raise ValueError("The dataset contains missing values.")


def main() -> None:
    """Download, validate, and save the sample dataset."""

    provider = YahooFinanceProvider()

    print(f"Downloading {PERIOD} of daily data for {TICKER}...")

    data = provider.get_daily_data(
        ticker=TICKER,
        period=PERIOD,
    )

    validate_data(data)

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    data.to_csv(
        OUTPUT_PATH,
        index=False,
    )

    print("Download completed successfully.")
    print(f"Rows: {len(data)}")
    print(f"Columns: {list(data.columns)}")
    print(f"First date: {data['date'].min().date()}")
    print(f"Last date: {data['date'].max().date()}")
    print(f"Duplicate dates: {data['date'].duplicated().sum()}")
    print(f"Missing values: {data.isna().sum().sum()}")
    print(f"Saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()

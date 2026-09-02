# EquityLens

EquityLens is a Streamlit research dashboard for general users exploring ASX
stocks. The first prototype will analyse at least 10 ASX tickers and will later
use a shared model trained across ASX 100 companies using the most recent five
years of daily data.

> EquityLens is an educational research tool, not financial advice. Its outputs
> must not be presented as guaranteed forecasts or buy/sell recommendations.

## Day 1 project contract

Day 1 establishes the repository and its boundaries. It deliberately does not
download market data, engineer indicators, or train a model.

The foundation is complete when:

- the package and Streamlit entry point import successfully;
- the smoke test and lint checks pass;
- secrets, virtual environments, local datasets, and model artefacts are not
  tracked by Git; and
- UI, data access, feature engineering, and modelling have separate modules.

## Set up

This project uses Python 3.11 or newer and [uv](https://docs.astral.sh/uv/) for
fast, reproducible environment management.

```bash
git clone <your-repository-url>
cd EquityLens
cp .env.example .env
uv sync --extra dev
```

Activate the environment if you want to run commands directly:

```bash
# macOS/Linux
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Run the app and quality checks:

```bash
PYTHONPATH=src uv run streamlit run streamlit_app.py
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

On Windows PowerShell, use
`$env:PYTHONPATH="src"; uv run streamlit run streamlit_app.py` for the app command.

## Structure

```text
EquityLens/
├── data/
│   ├── raw/                 # downloaded data; ignored by Git
│   └── processed/           # transformed data; ignored by Git
├── src/equitylens/
│   ├── ui/                  # Streamlit pages and presentation logic
│   ├── data/                # fetching, validation and storage
│   ├── features/            # reusable feature transformations
│   ├── models/              # training, evaluation and inference
│   └── config.py            # environment-based settings
├── tests/                   # automated checks
├── .env.example             # safe configuration template
├── pyproject.toml           # dependencies and tool configuration
└── streamlit_app.py         # thin application entry point
```

### Why the modules are separate

- **UI** decides how users select a ticker and see results. It should not know
  how prices are downloaded or a prediction is calculated.
- **Data** obtains and validates market data. It can later switch data provider
  without forcing changes to the dashboard or model.
- **Features** turns validated prices into model inputs. Keeping transformations
  independent makes them reusable during both training and prediction and helps
  prevent data leakage.
- **Models** trains, evaluates, saves, and applies the shared model. It consumes
  features through a clear contract rather than depending on Streamlit.

These boundaries make each part easier to test and let one part change without
silently breaking the others.

## Configuration and secrets

Safe defaults live in `src/equitylens/config.py`. Machine-specific settings are
read from environment variables prefixed with `EQUITYLENS_`. Copy
`.env.example` to `.env`; the real `.env` file is ignored by Git. Never place API
keys or credentials in source code or in `.env.example`.

## First commit

```bash
git add .
git commit -m "chore: initialise EquityLens project structure"
```

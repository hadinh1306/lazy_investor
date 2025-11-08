# Lazy Investor - DCA Strategy Calculator

A Streamlit-based calculator for analyzing Dollar-Cost Averaging (DCA) investment strategies with daily-compounded savings accounts.

## 🎯 What Problem Does This Solve?

Many investors receive lump sum amounts (tax returns, bonuses, inheritance) and face the question: **invest it all at once, or gradually over time?**

This tool helps you model a **gradual investment strategy** where you:
1. Park your lump sum in a high-interest savings account
2. Systematically invest fixed amounts at regular intervals (weekly, biweekly, or monthly)
3. Earn interest on your remaining cash while building your investment portfolio

This approach offers several benefits:
- **Reduces timing risk** by spreading purchases across multiple market conditions
- **Captures different price points** instead of betting on a single entry point
- **Earns interest** on uninvested capital while it waits
- **Provides psychological comfort** through gradual, systematic investing

## 🧪 What This Tool Is (and Isn't)

**This is:**
- A tool for behavioral optimization: understanding how investment cadence, timing, and cash management interact with market returns
- A calculator for comparing total returns from gradual DCA vs. lump sum approaches
- An educational tool to visualize the trade-offs between earning savings interest and market exposure

**This is NOT:**
- A tool to "beat" or "time" the market
- Investment advice (consult a financial advisor for personalized guidance)
- A guarantee of future performance (uses historical data only)

## ✨ Features

- **Portfolio diversification support**:
  - Invest in multiple ETFs/stocks with custom allocation percentages
  - Unlimited tickers per portfolio
  - Automatic rebalancing on each investment
  - **Supports partial share purchases** for precise allocation
- **Daily-compounded savings interest** calculation
- **Real market data** from Yahoo Finance (supports any stock/ETF ticker)
- **Flexible investment schedules** (twice a week, weekly, every two weeks, monthly)
- **Multi-scenario comparison**:
  - Save unlimited investment scenarios
  - Compare scenarios side-by-side in a summary table
  - Interactive line chart showing total value over time
  - Identify best-performing strategy automatically
- **Comprehensive return metrics**:
  - Total portfolio return (savings + investments)
  - Investment-only return
  - Savings interest earned
  - Return rate percentage
- **Detailed CSV export** with daily breakdown including:
  - Daily and cumulative interest earned
  - Investment transactions and share purchases per ticker
  - Portfolio value tracking across all holdings
  - Complete return calculations
- **Interactive UI** built with Streamlit and Plotly

## 📁 Project Structure

```
lazy_investor/
├── main.py              # Streamlit UI and visualization code
├── calculations.py      # Core calculation logic and data fetching
├── pyproject.toml       # Project dependencies
├── uv.lock              # Locked dependency versions
├── .python-version      # Python version (3.12)
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

### Code Organization

**`main.py`** - Visualization Layer
- User input forms and scenario management
- Interactive Plotly charts for multi-scenario comparison
- CSV export functionality with detailed daily breakdowns
- Streamlit app layout and UI components

**`calculations.py`** - Business Logic
- `download_stock_data()` - Fetches ETF/stock data from Yahoo Finance
- `calculate_dca_returns()` - Simulates DCA strategy with daily compounding
- Helper functions for interest rates, stock prices, and date handling
- Handles non-trading days (weekends/holidays) by forward-filling portfolio values

This separation keeps the visualization code clean and makes the calculation logic reusable and testable.

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- [uv](https://docs.astral.sh/uv/) package manager (recommended) or pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/hadinh1306/lazy_investor.git
   cd lazy_investor
   ```

2. **Install dependencies**

   Using `uv` (recommended):
   ```bash
   uv sync
   ```

   Or using pip:
   ```bash
   pip install -e .
   ```

### Running the App

Using `uv`:
```bash
uv run streamlit run main.py
```

Or using pip:
```bash
streamlit run main.py
```

The app will open in your default browser at `http://localhost:8501`

## 📊 How to Use

1. **Enter your investment parameters:**
   - **Scenario Name**: Give your strategy a memorable name (e.g., "Weekly $500 Diversified")
   - **Initial Savings Amount**: Your lump sum to invest
   - **Annual Savings Interest Rate**: Interest rate on your savings account (compounded daily)
   - **Investment Amount per Period**: Fixed amount to invest each period (set to 0 for savings-only)
   - **Investment Frequency**: Choose from:
     - Twice a week (every 3.5 days)
     - Weekly (every 7 days)
     - Every two weeks (every 14 days)
     - Monthly (every 30 days)
   - **Period Start/End Date**: Investment timeframe
   - **Portfolio Structure**: Build your diversified portfolio
     - Add unlimited tickers using the "➕ Add Ticker" button
     - Assign allocation percentage to each ticker
     - Percentages must total 100%
     - Example: VFV.TO (40%), QCN (20%), IEFA (20%), EEMV (20%)
     - **Note**: Partial shares are supported and will be purchased automatically

2. **Click "Calculate & Save"** to run the simulation and save the scenario
   - The app will validate that your portfolio allocations total 100%
   - Stock data will be downloaded for all tickers in your portfolio

3. **Compare scenarios:**
   - View all saved scenarios in a side-by-side comparison table
   - See which scenario has the best return rate (highlighted automatically)
   - Select scenarios using checkboxes to visualize on the interactive chart
   - Compare total value over time across multiple strategies

4. **Download detailed data:**
   - Click "Download CSV" to export daily breakdown for selected scenarios
   - CSV includes 14 columns with comprehensive metrics:
     - Portfolio structure (allocation percentages)
     - Daily interest earned, cumulative interest
     - Investment transactions across all tickers
     - Share purchases per ticker (supports partial shares)
     - Portfolio value aggregated across holdings
     - Total returns and return rates
   - Dictionary columns (Stock Prices, Shares Purchased, Total Shares Owned) show data per ticker
   - Use the expandable info section to see column definitions

## 📈 Example Use Case

**Scenario:** You receive a $26,000 tax return and want to invest it using DCA. You're considering both investment frequency and portfolio diversification strategies.

**Compare multiple strategies:**

1. **"Weekly $500 - 100% VFV"**
   - Park money in 2.5% APY savings account
   - Invest $500 every week
   - Portfolio: 100% VFV.TO (S&P 500)
   - Period: 2025-01-01 to 2025-10-31

2. **"Weekly $500 - Diversified"**
   - Same savings account (2.5% APY)
   - Invest $500 every week
   - Portfolio: VFV.TO 40%, QCN 20%, IEFA 20%, EEMV 20%
   - Same period
   - Each week: $200 → VFV.TO, $100 → QCN, $100 → IEFA, $100 → EEMV

3. **"Twice a week $250 - Diversified"**
   - Same savings account and portfolio allocation
   - Invest $250 twice a week (more frequent, smaller amounts)
   - Same period

**What the calculator shows:**

- **Comparison table**: Side-by-side metrics for all three strategies, including portfolio composition
- **Best performer**: Automatically highlights which strategy has the highest return rate
- **Visual comparison**: Interactive line chart showing how total value evolves over time for each strategy
- **Detailed insights**:
  - How much interest you earned on savings for each strategy
  - How many shares you accumulated for each ticker at different prices (partial shares supported)
  - Whether diversification improved or reduced returns
  - Impact of investment frequency on final returns
  - Your total return combining both savings interest and investment gains
  - Daily breakdown via CSV export for deeper analysis, including per-ticker allocation details

This allows you to make an informed decision about both **when** to invest (frequency) and **what** to invest in (diversification) based on actual market data rather than just theory.

### Key Insights from Portfolio Structure

By comparing concentrated vs. diversified portfolios, you can answer questions like:
- Does diversification reduce volatility in my returns?
- Which asset allocation performs best during my investment period?
- How much does adding international exposure (IEFA) or emerging markets (EEMV) affect returns?
- Is the complexity of managing multiple tickers worth the potential benefits?

## 🛠️ Dependencies

- **streamlit** (>=1.50.0) - Web app framework
- **pandas** (>=2.3.3) - Data manipulation and analysis
- **yfinance** (>=0.2.66) - Stock/ETF data fetching from Yahoo Finance
- **plotly** (>=5.18.0) - Interactive charting and visualizations

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs or issues
- Suggest new features
- Submit pull requests

## 📄 License

This project is open source and available for personal and educational use.

## ⚠️ Disclaimer

This tool is for educational and research purposes only. It uses historical market data and does not predict future returns. Past performance does not guarantee future results. Always consult with a qualified financial advisor before making investment decisions.

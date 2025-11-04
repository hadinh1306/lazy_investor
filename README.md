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

- **Daily-compounded savings interest** calculation
- **Real market data** from Yahoo Finance (supports any stock/ETF ticker)
- **Flexible investment schedules** (weekly, biweekly, monthly)
- **Comprehensive return metrics**:
  - Total portfolio return (savings + investments)
  - Investment-only return
  - Savings interest earned
  - Simple return rate over the period
- **Investment history tracking** showing every purchase date, price, and shares
- **Interactive UI** built with Streamlit

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
- User input forms
- Results display (metrics, tables, breakdowns)
- Streamlit app layout and UI components

**`calculations.py`** - Business Logic
- `download_stock_data()` - Fetches ETF/stock data from Yahoo Finance
- `calculate_dca_returns()` - Simulates DCA strategy with daily compounding
- Helper functions for interest rates, stock prices, and date handling

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

1. **Enter your parameters:**
   - Initial Savings Amount: Your lump sum to invest
   - Annual Savings Interest Rate: Interest rate on your savings account (compounded daily)
   - Investment Amount per Period: Fixed amount to invest each period
   - Investment Frequency: How often you invest (weekly/biweekly/monthly)
   - Period Start/End Date: Investment timeframe
   - ETF Ticker Symbol: Stock/ETF to invest in (e.g., VFV.TO, SPY, QQQ)

2. **Click "Calculate Returns"** to run the simulation

3. **Review the results:**
   - Summary metrics showing total returns and return rate
   - Detailed breakdown of savings vs. investment performance
   - Complete investment history with dates and prices

## 📈 Example Use Case

**Scenario:** You receive a $26,000 tax return and want to invest it in VFV.TO (Vanguard S&P 500 ETF).

**Strategy:**
- Park the money in a 4.5% APY savings account
- Invest $500 every week into VFV.TO
- Run for the full year (2024-01-01 to 2024-12-31)

**The calculator shows:**
- How much interest you earned on your savings
- How many shares you accumulated at different prices
- Your total return combining both savings interest and investment gains
- Whether this strategy outperformed a lump sum investment

## 🛠️ Dependencies

- **streamlit** (>=1.50.0) - Web app framework
- **pandas** (>=2.3.3) - Data manipulation
- **yfinance** (>=0.2.66) - Stock/ETF data fetching

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs or issues
- Suggest new features
- Submit pull requests

## 📄 License

This project is open source and available for personal and educational use.

## ⚠️ Disclaimer

This tool is for educational and research purposes only. It uses historical market data and does not predict future returns. Past performance does not guarantee future results. Always consult with a qualified financial advisor before making investment decisions.

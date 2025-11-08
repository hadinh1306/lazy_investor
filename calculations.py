"""
Calculation functions for DCA investment strategy with daily-compounded savings.
"""

import pandas as pd
import yfinance as yf


def download_stock_data(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Download stock/ETF data from Yahoo Finance.
    Assumptions:
        Input a single ticker.
        Period start and end are weekdays.

    Args:
        ticker: Stock/ETF ticker symbol (e.g., 'VFV.TO')
        start_date: Start date in 'YYYY-MM-DD' format
        end_date: End date in 'YYYY-MM-DD' format

    Returns:
        DataFrame with columns: date, ticker, open, close, volume

    Raises:
        ValueError: If no stock data is found for the given ticker
    """

    stock_data = yf.download(ticker, start=start_date, end=end_date, progress=False)

    if stock_data.empty:
        raise ValueError(f"No stock data found, make sure your ticker is correct: {ticker}")

    # Flatten MultiIndex columns if present
    if isinstance(stock_data.columns, pd.MultiIndex):
        # Get the ticker name from the MultiIndex
        ticker_name = stock_data.columns[0][1]

        # Flatten the MultiIndex by taking only the first level (Price)
        stock_data.columns = stock_data.columns.get_level_values(0)
    else:
        ticker_name = ticker

    # Reset index to make Date a column
    stock_data = stock_data.reset_index()

    stock_data['Ticker'] = ticker_name

    return stock_data


def calculate_daily_interest_rate(annual_rate: float) -> float:
    """
    Convert annual interest rate to daily rate.

    Args:
        annual_rate: Annual interest rate as percentage (e.g., 5 for 5%)

    Returns:
        Daily interest rate as decimal
    """
    return (annual_rate / 100) / 365


def get_investment_interval_days(frequency: str) -> int:
    """
    Convert investment frequency to number of days.

    Args:
        frequency: One of 'Twice a week', 'Weekly', 'Every two weeks', or 'Monthly'

    Returns:
        Number of days between investments
    """
    freq_days = {
        'Twice a week': 3.5,
        'Weekly': 7,
        'Every two weeks': 14,
        'Monthly': 30
    }
    return freq_days.get(frequency, 7)


def get_stock_price(stock_data: pd.DataFrame, date: pd.Timestamp) -> float:
    """
    Get the closing price for a specific date.

    Args:
        stock_data: DataFrame with columns [date, ticker, open, close, volume]
        date: Date to get price for

    Returns:
        Closing price as float, or None if date not found
    """
    # Filter the dataframe for the specific date
    matching_rows = stock_data[stock_data['Date'] == date]

    if matching_rows.empty:
        return None

    # Get the opening price from the first matching row
    stock_price = matching_rows['Close'].iloc[0]

    return stock_price


def calculate_dca_returns(
    initial_savings: float,
    annual_interest_rate: float,
    investment_amount: float,
    investment_frequency: str,
    portfolio_structure: dict,
    start_date: str,
    end_date: str
) -> dict:
    """
    Calculate returns from DCA strategy with daily-compounded savings and portfolio allocation.

    This function simulates a dollar-cost averaging investment strategy where:
    1. Money sits in a savings account earning daily compound interest
    2. At regular intervals, a fixed amount is withdrawn and invested across multiple ETFs
    3. Investment is split according to portfolio allocation percentages
    4. The investment grows based on actual market performance
    5. Partial shares can be purchased

    Use Cases:
    - Savings only: Set investment_amount = 0, portfolio_structure can be empty dict
    - Lump sum investment: Set initial_savings = lump_sum, investment_amount = lump_sum,
                           and ensure only one investment period fits in date range
    - DCA from savings: Set initial_savings > 0, investment_amount > 0
    - Single ticker: portfolio_structure = {'TICKER': 1.0}
    - Multi-ticker: portfolio_structure = {'TICKER1': 0.4, 'TICKER2': 0.6, ...}

    Args:
        initial_savings: Initial amount in savings account
        annual_interest_rate: Annual savings interest rate (%)
        investment_amount: Fixed amount to invest each period (can be 0 for savings-only)
        investment_frequency: 'Twice a week', 'Weekly', 'Every two weeks', or 'Monthly'
        portfolio_structure: Dict mapping ticker symbols to allocation percentages (as decimals)
                           Example: {'VFV.TO': 0.4, 'QCN': 0.2, 'IEFA': 0.2, 'EEMV': 0.2}
                           Must sum to 1.0 (100%). Can be empty if investment_amount = 0.
        start_date: Investment period start date (YYYY-MM-DD)
        end_date: Investment period end date (YYYY-MM-DD)

    Returns:
        dict: Contains all calculation results including:
            - initial_savings: Starting savings amount
            - total_invested: Total amount invested across all ETFs
            - num_investments: Number of investment transactions
            - total_shares: Dict of total shares purchased per ticker
            - final_stock_prices: Dict of ETF prices at end date
            - final_portfolio_value: Value of all ETF holdings at end
            - final_savings: Remaining savings balance
            - savings_interest_earned: Interest earned on savings
            - total_final_value: Total value (savings + investments)
            - total_return: Total dollar return
            - return_rate: Total return as percentage
            - investment_return: Return from ETF investments only
            - investment_return_rate: ETF return as percentage
            - investment_dates: List of all investment transactions
            - savings_history: Daily savings balance history
            - portfolio_value_history: Daily portfolio value history

    Raises:
        ValueError: If stock data cannot be downloaded or if portfolio_structure is invalid
    """
    # Validate portfolio structure
    if investment_amount > 0:
        if not portfolio_structure:
            raise ValueError("Portfolio structure cannot be empty when investment_amount > 0")

        total_allocation = sum(portfolio_structure.values())
        if not (0.99 <= total_allocation <= 1.01):  # Allow small floating point errors
            raise ValueError(f"Portfolio allocations must sum to 100%. Current sum: {total_allocation*100:.1f}%")
    # Download stock data for all tickers if we're making investments
    stock_data_dict = {}
    if investment_amount > 0:
        for ticker in portfolio_structure.keys():
            stock_data_dict[ticker] = download_stock_data(ticker, start_date, end_date)

    # Calculate daily interest rate
    daily_rate = calculate_daily_interest_rate(annual_interest_rate)

    # Get investment interval in days
    investment_interval = get_investment_interval_days(investment_frequency)

    # Initialize tracking variables
    current_savings = initial_savings
    total_shares_dict = {ticker: 0.0 for ticker in portfolio_structure.keys()}  # Shares per ticker
    last_known_price_dict = {ticker: 0.0 for ticker in portfolio_structure.keys()}  # Last known price per ticker
    total_invested = 0.0
    investment_dates = []
    savings_history = []
    portfolio_value_history = []
    portfolio_value = 0.0  # Initialize portfolio value

    # Create date range
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)
    date_range = pd.date_range(start=start, end=end, freq='D')

    days_since_investment = 0

    # Simulate day-by-day
    for current_date in date_range:
        # Apply daily interest to savings
        daily_interest = current_savings * daily_rate
        current_savings += daily_interest

        # Check if it's time to invest (only if investment_amount > 0)
        if investment_amount > 0:
            days_since_investment += 1

            if days_since_investment >= investment_interval and current_savings >= investment_amount:
                # Make investments across all tickers in portfolio
                investment_record = {
                    'date': current_date,
                    'total_amount': investment_amount,
                    'allocations': {}
                }

                can_invest = True
                # Check if all tickers have prices available
                for ticker in portfolio_structure.keys():
                    stock_price = get_stock_price(stock_data_dict[ticker], current_date)
                    if stock_price is None:
                        can_invest = False
                        break

                if can_invest:
                    # Invest in each ticker according to allocation
                    for ticker, allocation in portfolio_structure.items():
                        ticker_investment = investment_amount * allocation
                        stock_price = get_stock_price(stock_data_dict[ticker], current_date)
                        shares_purchased = ticker_investment / stock_price
                        total_shares_dict[ticker] += shares_purchased

                        investment_record['allocations'][ticker] = {
                            'amount': ticker_investment,
                            'price': stock_price,
                            'shares': shares_purchased
                        }

                    # Deduct full investment amount from savings
                    total_invested += investment_amount
                    current_savings -= investment_amount
                    investment_dates.append(investment_record)
                    days_since_investment = 0

        # Track savings balance
        savings_history.append({
            'date': current_date,
            'savings_balance': current_savings
        })

        # Calculate portfolio value (only if we have investments)
        if investment_amount > 0:
            # Calculate total portfolio value across all tickers with ticker-level forward-filling
            current_portfolio_value = 0.0

            for ticker, shares in total_shares_dict.items():
                if shares > 0:
                    current_stock_price = get_stock_price(stock_data_dict[ticker], current_date)

                    # Update last known price if we have a current price (trading day for this ticker)
                    if current_stock_price is not None:
                        last_known_price_dict[ticker] = current_stock_price

                    # Use last known price for this ticker (forward-fill at ticker level)
                    ticker_value = shares * last_known_price_dict[ticker]
                    current_portfolio_value += ticker_value

            portfolio_value = current_portfolio_value

            portfolio_value_history.append({
                'date': current_date,
                'portfolio_value': portfolio_value
            })
        else:
            # No investments, portfolio value is always 0
            portfolio_value_history.append({
                'date': current_date,
                'portfolio_value': 0
            })

    # Final calculations
    if investment_amount > 0:
        # Get final prices for all tickers
        final_stock_prices = {}
        final_portfolio_value = 0.0

        for ticker, shares in total_shares_dict.items():
            final_price = get_stock_price(stock_data_dict[ticker], date_range[-1])

            # If final price is None, get the last available price from the stock data
            if final_price is None:
                final_price = stock_data_dict[ticker]['Close'].iloc[-1]

            final_stock_prices[ticker] = final_price
            final_portfolio_value += shares * final_price
    else:
        # Savings-only scenario
        final_stock_prices = {}
        final_portfolio_value = 0

    final_savings = current_savings

    # Calculate savings interest earned
    savings_interest_earned = final_savings - (initial_savings - total_invested)

    # Total portfolio value (savings + investments)
    total_final_value = final_savings + final_portfolio_value

    # Calculate returns
    total_return = total_final_value - initial_savings
    return_rate = (total_return / initial_savings) * 100 if initial_savings > 0 else 0

    # Investment return
    investment_return = final_portfolio_value - total_invested
    investment_return_rate = (investment_return / total_invested) * 100 if total_invested > 0 else 0

    return {
        'initial_savings': initial_savings,
        'total_invested': total_invested,
        'num_investments': len(investment_dates),
        'total_shares': total_shares_dict,
        'final_stock_prices': final_stock_prices,
        'final_portfolio_value': final_portfolio_value,
        'final_savings': final_savings,
        'savings_interest_earned': savings_interest_earned,
        'total_final_value': total_final_value,
        'total_return': total_return,
        'return_rate': return_rate,
        'investment_return': investment_return,
        'investment_return_rate': investment_return_rate,
        'investment_dates': investment_dates,
        'savings_history': savings_history,
        'portfolio_value_history': portfolio_value_history
    }

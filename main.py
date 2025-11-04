"""
Streamlit app for Lazy Investor - DCA Strategy Calculator
"""

import streamlit as st
import pandas as pd
from datetime import datetime

from calculations import calculate_dca_returns


def main():
    """Main Streamlit app for DCA strategy visualization."""
    st.title("💰 Lazy Investor - DCA Strategy Calculator")
    st.write("Analyze your Dollar-Cost Averaging strategy with daily-compounded savings")

    # User Inputs
    st.subheader("📝 Investment Parameters")

    col1, col2 = st.columns(2)

    with col1:
        initial_savings = st.number_input(
            "Initial Savings Amount ($)",
            min_value=0.0,
            value=26000.0,
            step=1000.0,
            format="%.2f",
            help="Starting balance in your savings account"
        )

        investment_amount = st.number_input(
            "Investment Amount per Period ($)",
            min_value=0.0,
            value=500.0,
            step=50.0,
            format="%.2f",
            help="Fixed amount to invest each period"
        )

        start_date = st.date_input(
            "Period Start Date",
            value=datetime(2025, 1, 1),
            help="Start date for investment period"
        )

    with col2:
        annual_interest_rate = st.number_input(
            "Annual Savings Interest Rate (%)",
            min_value=0.0,
            max_value=100.0,
            value=4.5,
            step=0.1,
            format="%.2f",
            help="Annual interest rate (compounded daily)"
        )

        investment_frequency = st.selectbox(
            "Investment Frequency",
            options=['Weekly', 'Biweekly', 'Monthly'],
            index=0,
            help="How often you invest"
        )

        end_date = st.date_input(
            "Period End Date",
            value=datetime(2025, 10, 31),
            help="End date for investment period"
        )

    ticker = st.text_input(
        "ETF Ticker Symbol",
        value="VFV.TO",
        help="Stock/ETF ticker symbol (e.g., VFV.TO for Toronto Stock Exchange)"
    )

    # Calculate button
    if st.button("Calculate Returns", type="primary"):
        if initial_savings > 0 and investment_amount > 0:
            with st.spinner("Calculating your DCA returns..."):
                try:
                    results = calculate_dca_returns(
                        initial_savings=initial_savings,
                        annual_interest_rate=annual_interest_rate,
                        investment_amount=investment_amount,
                        investment_frequency=investment_frequency,
                        ticker=ticker,
                        start_date=start_date.strftime('%Y-%m-%d'),
                        end_date=end_date.strftime('%Y-%m-%d')
                    )

                    # Store results in session state
                    st.session_state['results'] = results
                    st.session_state['ticker'] = ticker

                except ValueError as e:
                    st.error(str(e))
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter valid amounts for initial savings and investment amount.")

    # Display results if they exist
    if 'results' in st.session_state:
        results = st.session_state['results']
        ticker = st.session_state.get('ticker', 'ETF')

        display_summary_metrics(results)
        display_return_breakdown(results)
        display_detailed_breakdown(results, ticker)
        display_investment_history(results)


def display_summary_metrics(results: dict):
    """Display summary metrics in a row of metric cards."""
    st.divider()
    st.subheader("📊 Summary")

    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

    with metric_col1:
        st.metric(
            label="Initial Investment",
            value=f"${results['initial_savings']:,.2f}"
        )

    with metric_col2:
        st.metric(
            label="Total End Value",
            value=f"${results['total_final_value']:,.2f}",
            delta=f"${results['total_return']:,.2f}"
        )

    with metric_col3:
        st.metric(
            label="Total Return",
            value=f"${results['total_return']:,.2f}",
            delta=f"{results['return_rate']:.2f}%"
        )

    with metric_col4:
        st.metric(
            label="Return Rate",
            value=f"{results['return_rate']:.2f}%"
        )


def display_return_breakdown(results: dict):
    """Display return breakdown table."""
    st.divider()
    st.subheader("📈 Return Breakdown")

    breakdown_data = {
        "Description": [
            "Initial Investment",
            "Total Value End of Period",
            "Total Return Value",
            "Return Rate"
        ],
        "Value": [
            f"${results['initial_savings']:,.2f}",
            f"${results['total_final_value']:,.2f}",
            f"${results['total_return']:,.2f}",
            f"{results['return_rate']:.2f}%"
        ]
    }

    df_breakdown = pd.DataFrame(breakdown_data)
    st.dataframe(df_breakdown, use_container_width=True, hide_index=True)


def display_detailed_breakdown(results: dict, ticker: str):
    """Display detailed breakdown of savings and investments."""
    st.divider()
    st.subheader("💡 Detailed Breakdown")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Savings Account:**")
        st.write(f"- Final Balance: ${results['final_savings']:,.2f}")
        st.write(f"- Interest Earned: ${results['savings_interest_earned']:,.2f}")
        st.write(f"- Total Withdrawn for Investments: ${results['total_invested']:,.2f}")

    with col2:
        st.write(f"**{ticker} Investment:**")
        st.write(f"- Number of Investments: {results['num_investments']}")
        st.write(f"- Total Invested: ${results['total_invested']:,.2f}")
        st.write(f"- Total Shares: {results['total_shares']:.4f}")
        st.write(f"- Final Share Price: ${results['final_stock_price']:.2f}")
        st.write(f"- Portfolio Value: ${results['final_portfolio_value']:,.2f}")
        st.write(f"- Investment Return: ${results['investment_return']:,.2f} ({results['investment_return_rate']:.2f}%)")


def display_investment_history(results: dict):
    """Display table of all investment transactions."""
    if results['investment_dates']:
        st.divider()
        st.subheader("📅 Investment History")

        investment_df = pd.DataFrame(results['investment_dates'])
        investment_df['date'] = pd.to_datetime(investment_df['date']).dt.strftime('%Y-%m-%d')
        investment_df['price'] = investment_df['price'].apply(lambda x: f"${x:.2f}")
        investment_df['shares'] = investment_df['shares'].apply(lambda x: f"{x:.4f}")
        investment_df['amount'] = investment_df['amount'].apply(lambda x: f"${x:.2f}")

        investment_df.columns = ['Date', 'Share Price', 'Shares Purchased', 'Amount Invested']

        st.dataframe(investment_df, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()

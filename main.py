"""
Streamlit app for Lazy Investor - DCA Strategy Calculator
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

from calculations import calculate_dca_returns


def main():
    """Main Streamlit app for DCA strategy visualization."""
    # Set page config for wide layout
    st.set_page_config(
        page_title="Lazy Investor - DCA Calculator",
        page_icon="💰",
        layout="wide"
    )

    st.title("💰 Lazy Investor - DCA Strategy Calculator")
    st.write("Compare different investment strategies by running multiple scenarios and viewing them side-by-side.")

    # Initialize saved scenarios in session state
    if 'saved_scenarios' not in st.session_state:
        st.session_state['saved_scenarios'] = {}

    display_main_interface()


def display_main_interface():
    """Display the unified calculator and comparison interface."""
    # Create main layout
    left_col, right_col = st.columns([1, 2])

    with left_col:
        # User Inputs
        st.subheader("📝 Investment Parameters")

        scenario_name = st.text_input(
            "Scenario Name",
            value="",
            placeholder="e.g., Weekly $500 DCA",
            help="Give this scenario a memorable name"
        )

        initial_savings = st.number_input(
            "Initial Savings Amount ($)",
            min_value=0.0,
            value=26000.0,
            step=1000.0,
            format="%.2f",
            help="Starting balance in your savings account"
        )

        annual_interest_rate = st.number_input(
            "Annual Savings Interest Rate (%)",
            min_value=0.0,
            max_value=100.0,
            value=4.5,
            step=0.1,
            format="%.2f",
            help="Annual interest rate (compounded daily)"
        )

        investment_amount = st.number_input(
            "Investment Amount per Period ($)",
            min_value=0.0,
            value=500.0,
            step=50.0,
            format="%.2f",
            help="Fixed amount to invest each period. Set to 0 for savings-only."
        )

        investment_frequency = st.selectbox(
            "Investment Frequency",
            options=['Weekly', 'Biweekly', 'Monthly'],
            index=0,
            help="How often you invest"
        )

        start_date = st.date_input(
            "Period Start Date",
            value=datetime(2025, 1, 1),
            help="Start date for investment period"
        )

        end_date = st.date_input(
            "Period End Date",
            value=datetime(2025, 10, 31),
            help="End date for investment period"
        )

        ticker = st.text_input(
            "ETF Ticker Symbol",
            value="VFV.TO",
            help="Stock/ETF ticker symbol (ignored if investment amount is 0)"
        )

        # Calculate button
        col1, col2 = st.columns([1, 1])

        with col1:
            if st.button("Calculate & Save", type="primary", use_container_width=True):
                if initial_savings > 0:
                    if not scenario_name:
                        st.warning("Please enter a scenario name")
                    elif scenario_name in st.session_state['saved_scenarios']:
                        st.warning("Scenario name already exists. Choose a different name.")
                    else:
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

                                # Save scenario immediately
                                save_scenario(scenario_name, results, {
                                    'initial_savings': initial_savings,
                                    'investment_amount': investment_amount,
                                    'investment_frequency': investment_frequency,
                                    'annual_interest_rate': annual_interest_rate,
                                    'start_date': start_date.strftime('%Y-%m-%d'),
                                    'end_date': end_date.strftime('%Y-%m-%d'),
                                    'ticker': ticker
                                })

                                # Store as current results
                                st.session_state['current_results'] = results
                                st.session_state['current_scenario_name'] = scenario_name

                                st.success(f"✅ Saved: {scenario_name}")
                                st.rerun()

                            except ValueError as e:
                                st.error(str(e))
                            except Exception as e:
                                st.error(f"An error occurred: {str(e)}")
                else:
                    st.warning("Please enter a valid initial savings amount.")

        with col2:
            if st.session_state.get('saved_scenarios'):
                if st.button("🗑️ Clear All", use_container_width=True):
                    st.session_state['saved_scenarios'] = {}
                    if 'current_results' in st.session_state:
                        del st.session_state['current_results']
                    if 'current_scenario_name' in st.session_state:
                        del st.session_state['current_scenario_name']
                    st.rerun()

    with right_col:
        # Display comparison section if there are saved scenarios
        saved_scenarios = st.session_state.get('saved_scenarios', {})
        if saved_scenarios:
            display_scenario_comparison(saved_scenarios)
        else:
            st.info("👈 Enter your investment parameters and click 'Calculate & Save' to see results")


def save_scenario(name: str, results: dict, params: dict):
    """Save a scenario to session state."""
    st.session_state['saved_scenarios'][name] = {
        'results': results,
        'params': params,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }


def display_scenario_comparison(saved_scenarios: dict):
    """Display comparison of all saved scenarios."""
    st.subheader(f"🔍 Scenario Comparison ({len(saved_scenarios)} saved)")

    # Create comparison table
    comparison_data = []
    for name in saved_scenarios.keys():
        scenario = saved_scenarios[name]
        results = scenario['results']
        params = scenario['params']

        comparison_data.append({
            'Scenario': name,
            'Initial': f"${results['initial_savings']:,.0f}",
            'Frequency': params['investment_frequency'],
            'Amount/Period': f"${params['investment_amount']:,.0f}",
            'Interest': f"{params['annual_interest_rate']}%",
            'Ticker': params['ticker'],
            'Final Value': f"${results['total_final_value']:,.0f}",
            'Total Return': f"${results['total_return']:,.0f}",
            'Return Rate': f"{results['return_rate']:.1f}%"
        })

    df_comparison = pd.DataFrame(comparison_data)
    st.dataframe(df_comparison, use_container_width=True, hide_index=True)

    # Highlight best performing scenario
    best_scenario = max(saved_scenarios.keys(), key=lambda name: saved_scenarios[name]['results']['return_rate'])
    st.success(f"🏆 Best Return Rate: **{best_scenario}** ({saved_scenarios[best_scenario]['results']['return_rate']:.1f}%)")

    # Scenario selection for visualization
    st.subheader("📈 Total Value Over Time")
    st.write("Select up to 3 scenarios to visualize:")

    # Use session state to track selected scenarios
    if 'selected_for_chart' not in st.session_state:
        # Default to first 3 scenarios
        st.session_state['selected_for_chart'] = list(saved_scenarios.keys())[:min(3, len(saved_scenarios))]

    # Create checkboxes for each scenario
    selected_scenarios = []
    for name in saved_scenarios.keys():
        # Check if this scenario should be checked
        is_checked = name in st.session_state['selected_for_chart']

        # Disable checkbox if 3 are already selected and this one isn't checked
        is_disabled = len(st.session_state['selected_for_chart']) >= 3 and not is_checked

        if st.checkbox(
            name,
            value=is_checked,
            key=f"chart_select_{name}",
            disabled=is_disabled
        ):
            selected_scenarios.append(name)

    # Update session state
    st.session_state['selected_for_chart'] = selected_scenarios

    if selected_scenarios:
        if len(selected_scenarios) > 3:
            st.warning("⚠️ Please select up to 3 scenarios only")
        else:
            display_comparison_chart(saved_scenarios, selected_scenarios)
    else:
        st.info("Select at least one scenario to visualize")


def display_comparison_chart(saved_scenarios: dict, selected_scenarios: list):
    """Display interactive line chart comparing total value over time for selected scenarios."""
    fig = go.Figure()

    for name in selected_scenarios:
        scenario = saved_scenarios[name]
        results = scenario['results']

        # Get daily history
        savings_history = pd.DataFrame(results['savings_history'])
        portfolio_history = pd.DataFrame(results['portfolio_value_history'])

        # Merge and calculate total value
        combined_df = savings_history.merge(portfolio_history, on='date', how='left')
        combined_df['portfolio_value'] = combined_df['portfolio_value'].fillna(0)
        combined_df['total_value'] = combined_df['savings_balance'] + combined_df['portfolio_value']
        combined_df['date'] = pd.to_datetime(combined_df['date'])

        # Format values for display
        combined_df['formatted_value'] = combined_df['total_value'].apply(lambda x: f"${x:,.0f}")

        # Add trace for this scenario
        fig.add_trace(go.Scatter(
            x=combined_df['date'],
            y=combined_df['total_value'],
            mode='lines',
            name=name,
            line=dict(width=2),
            hovertemplate='<b>%{meta}</b>: %{customdata}<extra></extra>',
            meta=[name] * len(combined_df),
            customdata=combined_df['formatted_value']
        ))

    # Update layout
    fig.update_layout(
        xaxis_title=None,
        yaxis_title="Total Value ($)",
        hovermode='x unified',
        height=500,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=0, r=0, t=30, b=0),
        xaxis=dict(
            showticklabels=False,  # Hide x-axis labels
            showgrid=True
        ),
        yaxis=dict(
            showgrid=True,
            tickformat='$,.0f'
        )
    )

    st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()

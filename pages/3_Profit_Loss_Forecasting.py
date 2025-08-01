import streamlit as st
import pandas as pd
import numpy as np

# --- Page Security ---
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

if st.session_state.get("user_type") != "gov":
    st.error("ACCESS DENIED: This tool is available for Government Login only.")
    st.write("Please log out and sign in with government credentials from the main portal.")
    st.stop()

# --- Simple Forecasting Function ---
# In a real-world scenario with a trained model, this function would be replaced.
# For this project, a projection based on the last year's trend is a robust and clear demonstration.
def project_future_trends(df, years=5):
    """Projects future values based on the last year's average daily growth."""
    forecasts = {}
    
    # Define the columns we want to forecast
    columns_to_forecast = [
        'average_selling_price_usd', 
        'silicon_wafer_cost_usd', 
        'energy_cost_per_kwh_usd', 
        'total_daily_labor_cost_usd'
    ]
    
    for col in columns_to_forecast:
        # Take the last 365 days of data to calculate the trend
        last_year_data = df.tail(365)
        
        # Calculate the average daily percentage change
        daily_growth = last_year_data[col].pct_change().mean()
        
        # Project this trend forward for 5 years
        last_value = last_year_data[col].iloc[-1]
        yearly_growth_factor = (1 + daily_growth) ** 365
        
        future_values = [last_value * (yearly_growth_factor ** year) for year in range(1, years + 1)]
        forecasts[col] = np.array(future_values)
        
    return forecasts

# --- Load the Synthetic Dataset ---
try:
    df_historical = pd.read_csv("data/synthetic_fab_data.csv")
    df_historical['date'] = pd.to_datetime(df_historical['date'])
except FileNotFoundError:
    st.error("Dataset not found. Please run `generate_synthetic_data.py` first to create the required dataset.")
    st.stop()

# --- Page UI ---
st.title("📈 Profit & Loss Forecasting Tool")
st.markdown("---")
st.info("This tool projects a 5-year financial forecast for a new semiconductor fab based on historical trends and your operational assumptions.")

# --- User Input Sidebar ---
st.sidebar.header("Financial & Operational Assumptions")

initial_capex = st.sidebar.slider(
    "Initial CAPEX Investment (Billion USD)", 
    min_value=5.0, max_value=20.0, value=10.0, step=0.5,
    help="The total upfront cost to build and equip the fabrication plant."
)
capacity_wpm = st.sidebar.slider(
    "Production Capacity (Wafer Starts Per Month)", 
    min_value=10000, max_value=100000, value=50000, step=5000,
    help="The number of silicon wafers the fab can process each month."
)
chips_per_wafer = st.sidebar.slider(
    "Average Chips (Dies) per Wafer", 
    min_value=100, max_value=1000, value=400, step=10,
    help="The average number of final chips produced from a single wafer. This depends on chip size and yield."
)

if st.sidebar.button("Run 5-Year Forecast", type="primary", use_container_width=True):
    st.header("5-Year Financial Projections")

    # --- Calculations ---
    years = np.arange(1, 6)
    
    # Get the forecasted values for revenue and cost drivers
    forecasts = project_future_trends(df_historical, years=5)
    
    # Calculate total annual production numbers
    annual_chip_production = capacity_wpm * 12 * chips_per_wafer
    annual_wafer_production = capacity_wpm * 12
    
    # Calculate Total Annual Revenue
    annual_revenue = (annual_chip_production * forecasts['average_selling_price_usd']) / 1_000_000_000 # Convert to Billions
    
    # Calculate Total Annual OPEX
    annual_material_cost = (annual_wafer_production * forecasts['silicon_wafer_cost_usd']) / 1_000_000_000
    annual_labor_cost = (forecasts['total_daily_labor_cost_usd'] * 365) / 1_000_000_000
    # Assuming a constant, high energy usage for a fab of this size for simplicity
    annual_energy_cost = (500_000_000 * forecasts['energy_cost_per_kwh_usd']) / 1_000_000_000 # 500 Million kWh/year
    
    annual_opex = annual_material_cost + annual_labor_cost + annual_energy_cost
    
    # Calculate Final Profit & Loss
    depreciation = initial_capex / 5 # Simple straight-line depreciation over 5 years
    annual_profit_loss = annual_revenue - annual_opex - depreciation
    cumulative_profit_loss = np.cumsum(annual_profit_loss)

    # --- Display Results ---
    df_forecast = pd.DataFrame({
        "Year": years,
        "Projected Revenue (Billion USD)": annual_revenue,
        "Projected OPEX (Billion USD)": annual_opex,
        "Annual Profit/Loss (Billion USD)": annual_profit_loss,
        "Cumulative Profit/Loss (Billion USD)": cumulative_profit_loss
    })

    st.subheader("Financial Performance Over Time")
    st.line_chart(df_forecast, x="Year", y=["Projected Revenue (Billion USD)", "Projected OPEX (Billion USD)", "Cumulative Profit/Loss (Billion USD)"])

    st.subheader("Forecast Summary Table")
    st.dataframe(df_forecast.style.format("{:.2f}"))

    st.subheader("Key Financial Metrics")
    col1, col2 = st.columns(2)
    
    with col1:
        try:
            # Find the first year where cumulative profit is positive
            break_even_year = df_forecast[df_forecast["Cumulative Profit/Loss (Billion USD)"] >= 0]["Year"].iloc[0]
            st.success(f"**Projected Break-Even Point:** Year {break_even_year}")
        except IndexError:
            st.warning("**Warning:** The project does not reach profitability within the 5-year forecast period under these assumptions.")

    with col2:
        total_profit = df_forecast["Cumulative Profit/Loss (Billion USD)"].iloc[-1]
        st.metric("Total 5-Year Net Result (Billion USD)", f"{total_profit:.2f}")
else:
    st.info("Adjust the assumptions in the sidebar and click 'Run 5-Year Forecast' to see the financial projections.")
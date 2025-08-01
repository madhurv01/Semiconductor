import pandas as pd
import numpy as np
from datetime import datetime, timedelta

print("Starting synthetic data generation...")

# --- Configuration Parameters You Can Tune ---
num_rows = 1500  # <--- YOU CAN CHANGE THIS NUMBER. Set to 1500 to exceed the 700-row minimum.

# Revenue Parameters
base_asp = 8.50      # Average selling price of a chip in USD
asp_growth = 0.0005  # Slight daily growth trend
asp_volatility = 0.01  # Daily price fluctuation

# Cost Parameters
base_wafer_cost = 250      # Cost per silicon wafer
wafer_cost_growth = 0.0001 # Slow, steady growth

base_energy_cost_kwh = 0.09 # Industrial electricity rate in USD
energy_cost_growth = 0.00015
energy_volatility = 0.005

base_labor_cost_per_day = 500000 # Aggregate daily labor cost for the fab
labor_cost_growth = 0.0002       # Reflects salary inflation

# --- Data Generation ---

# Create a date range ending today
end_date = datetime.now()
start_date = end_date - timedelta(days=num_rows - 1)
dates = pd.date_range(start=start_date, end=end_date, freq='D')

# 1. Generate Revenue Data
# Simulate a "random walk" with an upward drift for the average selling price
asp_daily_returns = np.random.normal(loc=asp_growth, scale=asp_volatility, size=num_rows)
synthetic_asp = base_asp * np.cumprod(1 + asp_daily_returns)

# 2. Generate Cost Data
wafer_cost_returns = np.random.normal(loc=wafer_cost_growth, scale=0.001, size=num_rows)
synthetic_wafer_cost = base_wafer_cost * np.cumprod(1 + wafer_cost_returns)

energy_cost_returns = np.random.normal(loc=energy_cost_growth, scale=energy_volatility, size=num_rows)
synthetic_energy_cost = base_energy_cost_kwh * np.cumprod(1 + energy_cost_returns)

labor_cost_returns = np.random.normal(loc=labor_cost_growth, scale=0.0005, size=num_rows)
synthetic_labor_cost = base_labor_cost_per_day * np.cumprod(1 + labor_cost_returns)

# --- Assemble the DataFrame ---
df = pd.DataFrame({
    'date': dates,
    'average_selling_price_usd': synthetic_asp,
    'silicon_wafer_cost_usd': synthetic_wafer_cost,
    'energy_cost_per_kwh_usd': synthetic_energy_cost,
    'total_daily_labor_cost_usd': synthetic_labor_cost
})

# --- Save to CSV ---
output_path = 'data/synthetic_fab_data.csv'
df.to_csv(output_path, index=False)

print(f"Successfully generated synthetic dataset with {len(df)} rows.")
print(f"File saved to: {output_path}")
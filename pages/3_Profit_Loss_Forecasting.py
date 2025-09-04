import streamlit as st
import pandas as pd
import numpy as np
import base64
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model

# --- Page Security ---
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

if st.session_state.get("user_type") != "gov":
    st.error("ACCESS DENIED: This tool is available for Government Login only.")
    st.write("Please log out and sign in with government credentials from the main portal.")
    st.stop()

# --- NEW: Function to embed a dedicated background image for this page ---
def add_page_bg(image_file):
    try:
        with open(image_file, "rb") as f:
            encoded_string = base64.b64encode(f.read()).decode()
        st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/jpeg;base64,{encoded_string});
            background-size: cover;
            background-position: center;
        }}
        /* Style for containers to make them glass-like and readable */
        [data-testid="stVerticalBlock"], [data-testid="stHorizontalBlock"] {{
            background: rgba(10, 25, 47, 0.45); /* Highly transparent */
            backdrop-filter: blur(5px);
            -webkit-backdrop-filter: blur(5px);
            border-radius: 10px;
            padding: 20px;
            border: 1px solid rgba(0, 168, 232, 0.2);
            margin-bottom: 20px;
        }}
        /* Enhance text readability with a stronger shadow */
        h1, h2, h3, h4, p, .st-emotion-cache-1yy083c, .st-emotion-cache-1629p8f, .st-emotion-cache-1njjmv6, .st-emotion-cache-1r6slb0, .st-emotion-cache-1hg5474, .st-emotion-cache-1q8dd3i {{
             text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.8);
        }}
        </style>
        """,
        unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.warning("Background image 'prof.jpg' not found. Please add it to the 'images' folder.")

# --- Call the function to set the background ---
add_page_bg("images/prof.jpg")

# --- AI Model Loading ---
@st.cache_resource
def load_ai_model():
    try:
        model = load_model("model/fab_lstm_forecaster.h5")
        return model
    except (FileNotFoundError, IOError):
        st.error("Trained AI model not found. Please run `train_forecasting_model.py` first to create the model.")
        return None

model = load_ai_model()

# --- AI Forecasting Function ---
def forecast_with_ai(df, years=5):
    data = df[['average_selling_price_usd', 'silicon_wafer_cost_usd', 'energy_cost_per_kwh_usd', 'total_daily_labor_cost_usd']].values
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)
    
    sequence_length = 60
    last_sequence = scaled_data[-sequence_length:]
    current_batch = last_sequence.reshape(1, sequence_length, 4)
    
    future_predictions = []
    
    for i in range(365 * years):
        next_prediction = model.predict(current_batch, verbose=0)
        future_predictions.append(next_prediction[0])
        current_batch = np.append(current_batch[:, 1:, :], [[next_prediction[0]]], axis=1)
        
    predicted_values = scaler.inverse_transform(future_predictions)
    
    yearly_forecasts = {}
    df_preds = pd.DataFrame(predicted_values, columns=['average_selling_price_usd', 'silicon_wafer_cost_usd', 'energy_cost_per_kwh_usd', 'total_daily_labor_cost_usd'])
    
    for i, year in enumerate(range(1, years + 1)):
        yearly_data = df_preds.iloc[i*365 : (i+1)*365]
        for col in yearly_data.columns:
            if col not in yearly_forecasts:
                yearly_forecasts[col] = []
            yearly_forecasts[col].append(yearly_data[col].mean())
            
    for col in yearly_forecasts:
        yearly_forecasts[col] = np.array(yearly_forecasts[col])
        
    return yearly_forecasts

# --- Load the Dataset ---
try:
    df_historical = pd.read_csv("data/synthetic_fab_data.csv")
    df_historical['date'] = pd.to_datetime(df_historical['date'])
except FileNotFoundError:
    st.error("Dataset not found. Please run `generate_synthetic_data.py` first.")
    st.stop()

# --- Page UI ---
st.title("🧠 AI-Powered Profit & Loss Forecasting")
st.markdown("---")
st.info("This tool uses a trained LSTM neural network to project a 5-year financial forecast based on historical data and your operational assumptions.")

st.sidebar.header("Financial & Operational Assumptions")
initial_capex = st.sidebar.slider("Initial CAPEX Investment (Billion USD)", 5.0, 20.0, 10.0, 0.5)
capacity_wpm = st.sidebar.slider("Production Capacity (Wafer Starts Per Month)", 10000, 100000, 50000, 5000)
chips_per_wafer = st.sidebar.slider("Average Chips per Wafer", 100, 1000, 400, 10)

if model is not None and st.sidebar.button("Run AI Forecast", type="primary", use_container_width=True):
    with st.spinner("Running AI model to generate 5-year forecast... This may take a moment."):
        years = np.arange(1, 6)
        forecasts = forecast_with_ai(df_historical)
        
        annual_chip_production = capacity_wpm * 12 * chips_per_wafer
        annual_wafer_production = capacity_wpm * 12
        
        annual_revenue = (annual_chip_production * forecasts['average_selling_price_usd']) / 1_000_000_000
        annual_material_cost = (annual_wafer_production * forecasts['silicon_wafer_cost_usd']) / 1_000_000_000
        annual_labor_cost = (forecasts['total_daily_labor_cost_usd'] * 365) / 1_000_000_000
        annual_energy_cost = (500_000_000 * forecasts['energy_cost_per_kwh_usd']) / 1_000_000_000
        
        annual_opex = annual_material_cost + annual_labor_cost + annual_energy_cost
        depreciation = initial_capex / 5
        annual_profit_loss = annual_revenue - annual_opex - depreciation
        cumulative_profit_loss = np.cumsum(annual_profit_loss)

        df_forecast = pd.DataFrame({
            "Year": years,
            "Projected Revenue (Billion USD)": annual_revenue,
            "Projected OPEX (Billion USD)": annual_opex,
            "Annual Profit/Loss (Billion USD)": annual_profit_loss,
            "Cumulative Profit/Loss (Billion USD)": cumulative_profit_loss
        })

    st.header("5-Year Financial Projections (Generated by AI)")
    st.subheader("Financial Performance Over Time")
    st.line_chart(df_forecast, x="Year", y=["Projected Revenue (Billion USD)", "Projected OPEX (Billion USD)", "Cumulative Profit/Loss (Billion USD)"])

    st.subheader("Forecast Summary Table")
    st.dataframe(df_forecast.style.format("{:.2f}"))

    st.subheader("Key Financial Metrics")
    col1, col2 = st.columns(2)
    with col1:
        try:
            break_even_year = df_forecast[df_forecast["Cumulative Profit/Loss (Billion USD)"] >= 0]["Year"].iloc[0]
            st.success(f"**Projected Break-Even Point:** Year {break_even_year}")
        except IndexError:
            st.warning("**Warning:** The project does not reach profitability within the 5-year forecast period.")

    with col2:
        total_profit = df_forecast["Cumulative Profit/Loss (Billion USD)"].iloc[-1]
        st.metric("Total 5-Year Net Result (Billion USD)", f"{total_profit:.2f}")

elif model is None:
    pass
else:
    st.info("Adjust the assumptions in the sidebar and click 'Run AI Forecast' to generate the financial projections.")
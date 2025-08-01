import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import os

print("--- AI Model Training Script Started ---")

# --- 1. Load and Preprocess the Data ---
try:
    df = pd.read_csv("data/synthetic_fab_data.csv")
    print(f"Loaded dataset with {len(df)} rows.")
except FileNotFoundError:
    print("Error: synthetic_fab_data.csv not found. Please run generate_synthetic_data.py first.")
    exit()

# We will forecast all four key metrics
data = df[['average_selling_price_usd', 'silicon_wafer_cost_usd', 'energy_cost_per_kwh_usd', 'total_daily_labor_cost_usd']].values

# Normalize the data: LSTMs work best with values between 0 and 1
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data)

# --- 2. Create Training Sequences ---
# We will use the last 60 days of data to predict the next day
sequence_length = 60
X_train, y_train = [], []

for i in range(sequence_length, len(scaled_data)):
    X_train.append(scaled_data[i-sequence_length:i, :])
    y_train.append(scaled_data[i, :])

X_train, y_train = np.array(X_train), np.array(y_train)

# Reshape the data for the LSTM model [samples, timesteps, features]
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], X_train.shape[2]))
print(f"Created training data with shape: {X_train.shape}")

# --- 3. Build the LSTM Model ---
model = Sequential()
# Input layer
model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))
# Hidden layer
model.add(LSTM(units=50, return_sequences=False))
# Output layer (predicting 4 features)
model.add(Dense(units=4))

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')
print("LSTM model built successfully.")
model.summary()

# --- 4. Train the Model ---
print("\nStarting model training... (This may take a few minutes)")
# epochs=1 is fast for a demonstration. For higher accuracy, you could increase this to 5 or 10.
history = model.fit(X_train, y_train, epochs=1, batch_size=32, verbose=1)
print("Model training complete.")

# --- 5. Save the Trained Model ---
# Ensure the model directory exists
if not os.path.exists('model'):
    os.makedirs('model')

model.save('model/fab_lstm_forecaster.h5')
print("Trained model saved successfully to 'model/fab_lstm_forecaster.h5'")
print("--- AI Model Training Script Finished ---")